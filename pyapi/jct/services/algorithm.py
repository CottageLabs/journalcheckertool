from asyncio import ALL_COMPLETED

from jct.models import Compliance, Funder, JournalDAO, InstitutionDAO, Check, Unknown, UnknownDAO
from jct.models.compliance import Compliance

SELF_ARCHIVING = "self_archiving"
FULLY_OA = "fully_oa"
HYBRID = "hybrid"
TA = "ta"

ALL_CHECKS = [
    SELF_ARCHIVING,
    FULLY_OA,
    HYBRID,
    TA
]

class AlgorithmService:
    def calculate(self, issn: str, funder: Funder, ror: str = None, checks: list = None):
        """
        Calculate the algorithm for the given ISSNs, RORs, and funders
        :param issns: a list of ISSNs
        :param rors: a list of RORs
        :param funders: a list of funders
        :return: a JSON response with the calculated algorithm
        """
        if checks is None:
            checks = ALL_CHECKS

        compliance = Compliance()

        journal = JournalDAO.get(issn)
        institution = InstitutionDAO.get(ror)

        compliance.journal = journal
        compliance.institution = institution
        compliance.funder = funder

        for route, route_options in funder.active_routes:
            if route not in checks:
                continue

            check = None
            match route:
                case "self_archiving":
                    check = self.self_archiving(compliance, route_options)
                case "fully_oa":
                    check = self.fully_oa(compliance, route_options)
                case "hybrid":
                    check = self.hybrid(compliance, route_options)
                case "ta":
                    check = self.ta(compliance, route_options)

            if check:
                if check.unknown:
                    unknown = Unknown(journal, funder, institution, check)
                    UnknownDAO.save(unknown)
                compliance.add_check(check)

        self.cards_for_display(compliance)

        compliance.end_check()

    def self_archiving(self, compliance, route_options):
        return None

    def fully_oa(self, compliance, route_options):
        journal = compliance.journal
        check = Check(FULLY_OA, issn=journal.requested_issn)

        if journal.oa_exception:
            check.log("FullOA.Exception")
            caveat = journal.get_oa_exception_caveat(compliance.funder)
            check.qualifications = [{"oa_exception_caveat": {"caveat": caveat}}]
            return check

        check.log("FullOA.NoException")

        if journal.in_doaj:
            check.log("FullOA.InDOAJ")
            if not journal.has_doaj_licences:
                check.log("FullOA.Unknown", {"missing": ["license"]})
                check.unknown = True
            else:
                matching_licences = journal.doaj_licence_matches(route_options.get("license", []))
                if len(matching_licences) > 0:
                    check.log("FullOA.Compliant", {"licence": matching_licences})
                    check.compliant = True
                else:
                    check.log("FullOA.NonCompliant", {"licence": matching_licences})
                    check.compliant = False
            return check

        check.log("FullOA.NotInDOAJ")

        if journal.in_progress_doaj:
            check.log("FullOA.InProgressDOAJ")
            check.compliant = True
            check.qualifications = [{"doaj_under_review": {}}]
            # FIXME: technically, this should also log "FullOA.Compliant"
        else:
            check.log("FullOA.NotInProgressDOAJ")
            check.compliant = False

        return check

    def hybrid(self, compliance, route_options):
        return None

    def ta(self, compliance, route_options):
        return None

    def cards_for_display(self, compliance):
        pass