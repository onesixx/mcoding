import subprocess


def teaser():
    untrusted_input = "&calc.exe"
    subprocess.run(["echo_args.bat", untrusted_input])


def shell_ex():
    subprocess.run(
        ["python.exe", "-c", "import sys; print(sys.argv)", "&", "echo", "LOL"],
        shell=False,
    )
    subprocess.run(
        ["python.exe", "-c", "import sys; print(sys.argv)", "&", "echo", "LOL"],
        shell=True,
    )
    subprocess.run(
        ["cmd.exe", "/c", "python.exe", "-c", "import sys; print(sys.argv)", "&", "echo", "LOL"],
        shell=False,
    )


def obviously_bad():
    untrusted_input = "&calc.exe"
    subprocess.run(["python.exe", "-m", "timeit", untrusted_input], shell=True)


def maybe_ok():
    untrusted_input = "&calc.exe"
    subprocess.run(["python.exe", "-m", "timeit", untrusted_input], shell=False)


def the_cve():
    untrusted_input = "&calc.exe"
    subprocess.run(["echo_args.bat", untrusted_input], shell=False)


def literally_noone():
    untrusted_input = "calc.exe"
    subprocess.run(["cmd.exe", "/c",  untrusted_input], shell=False)


def main():
    teaser()
    # shell_ex()
    # obviously_bad()
    # maybe_ok()
    # the_cve()
    # literally_noone()


if __name__ == "__main__":
    main()
