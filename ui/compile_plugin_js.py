import os, argparse

read_files = ["i_am_a_widget", "api_endpoint", "clinput", "jct", "funders", "find_out_more", "feedback", "plugin"]

def compile(env=""):
    with open(os.path.join("static", "js", "jct_plugin.js"), "w") as outfile:
        for f in read_files:
            if f == "api_endpoint" and env != "":
                f = f + "_" + env
            with open(os.path.join("static", "js", f + ".js"), "r") as infile:
                print("reading... {}".format(f))
                outfile.write("\n// -------- " + f + " --------\n\n")
                outfile.write(infile.read())
                outfile.write("\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compile the widget')
    parser.add_argument("-e", '--environment', type=str, default="",
                        help='environment to compile the widget for.  No argument defaults to production')

    args = parser.parse_args()
    compile(args.environment)