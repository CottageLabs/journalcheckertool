import os, yaml, json

from jctdata.indexes.indexer import Indexer
from jctdata import resolver
from jctdata import settings

from datetime import datetime
from copy import deepcopy


class FunderLanguage(Indexer):
    ID = "funder_language"
    SOURCES = ["funderdb"]

    def gather(self):
        print('FUNDER_LANGUAGE: Gathering data for funder language packs from sources: {x}'.format(x=",".join(self.SOURCES)))
        paths = resolver.gather_data(self.SOURCES, regather=False, reanalyse=True)
        print("FUNDER_LANGUAGE: funderdb source: " + paths.get("funderdb", {}).get("origin", "no funderdb source"))

    def analyse(self):
        print("FUNDER_LANGUAGE: Preparing funder language packs")

        dir = datetime.strftime(datetime.utcnow(), settings.DIR_DATE_FORMAT)
        fldir = os.path.join(self.dir, dir)
        analyse_dir = os.path.join(fldir, "analyse")
        os.makedirs(analyse_dir, exist_ok=True)

        funderdb_paths = resolver.SOURCES[self.SOURCES[0]].current_paths()
        funderdb_dir = funderdb_paths.get("origin")

        default_base = os.path.join(funderdb_dir, "default", "lang")
        base_langs = self._compile_multilang(default_base, "en")

        for funder_dir in os.listdir(os.path.join(funderdb_dir, "funders")):
            funder_lang_dir = os.path.join(funderdb_dir, "funders", funder_dir, "lang")
            funder_langs = self._compile_multilang(funder_lang_dir, "en")

            # where the funder has specified a language pack, layer it over the base language pack
            full_funder_langs = {}
            for lang, build in funder_langs.items():
                if lang in base_langs:
                    full_funder_langs[lang] = self._merge(base_langs[lang], build)
                else:
                    full_funder_langs[lang] = self._merge(base_langs["en"], build)

            # for any languages that the funder has not overridden, layer their "en" language over the top
            # of the default language for that language code
            for lang, build in base_langs.items():
                if lang not in full_funder_langs:
                    if "en" in funder_langs:
                        full_funder_langs[lang] = self._merge(build, funder_langs["en"])
                    else:
                        full_funder_langs[lang] = build

            for lang, build in full_funder_langs.items():
                with open(os.path.join(analyse_dir, funder_dir + "__" + lang + ".json"), "w") as o:
                    o.write(json.dumps(build, indent=2))

        print("FUNDER_LANGUAGE: Funder Language packs built")

    def assemble(self):
        print("FUNDER_LANGUAGE: Assembling funder language packs index")

        fldir = os.path.join(self.dir, self.current_dir())
        outfile = os.path.join(fldir, "funder_language.json")
        analyse_dir = os.path.join(fldir, "analyse")

        with open(outfile, "w") as o:
            for lang_file in os.listdir(analyse_dir):
                langfile_path = os.path.join(analyse_dir, lang_file)
                with open(langfile_path, "r") as f:
                    data = json.loads(f.read())
                data["id"] = lang_file.rsplit(".")[0]
                o.write(json.dumps(data) + "\n")

        print("FUNDER_LANGUAGE: Funder Language packs index data prepared")

        self._cleanup()

    def _compile_multilang(self, base_dir, base_lang):
        if not os.path.exists(base_dir):
            print("FUNDER_LANGUAGE: no specific language pack at {x}".format(x=base_dir))
            return {}

        print("FUNDER_LANGUAGE: compiling for multiple languages in {x} (base language {y})".format(x=base_dir, y=base_lang))
        base_lang_dir = os.path.join(base_dir, base_lang)
        base_lang_build = self._compile_dir(base_lang_dir)

        langs = {
            base_lang: base_lang_build
        }

        alt_langs = [x for x in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, x)) and x != base_lang]
        for alt in alt_langs:
            lang_dir = os.path.join(base_dir, alt)
            lang_build = self._compile_dir(lang_dir)
            lang_full = self._merge(base_lang_build, lang_build)
            langs[alt] = lang_full

        return langs

    def _compile_dir(self, path):
        print("FUNDER_LANGUAGE: compiling language dir {x}".format(x=path))
        compiled = {}
        if not os.path.exists(path):
            return compiled
        for entry in os.listdir(path):
            if not os.path.isdir(os.path.join(path, entry)):
                with open(os.path.join(path, entry)) as y:
                    data = yaml.load(y.read(), Loader=yaml.BaseLoader)
                key = entry.split(".")[0]
                compiled[key] = data

            else:
                compiled[entry] = self._compile_dir(os.path.join(path, entry))
        return compiled

    def _merge(self, base, overlay):
        result = deepcopy(base)
        for k, v in overlay.items():
            if isinstance(v, dict):
                if k in base:
                    result[k] = self._merge(base[k], overlay[k])
                else:
                    result[k] = overlay[k]
            else:
                result[k] = overlay[k]
        return result