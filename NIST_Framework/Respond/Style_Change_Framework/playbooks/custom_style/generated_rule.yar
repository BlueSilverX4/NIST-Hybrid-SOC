rule EvilPayload_Check {
    meta:
        author = "CustomStyle_SOAR"
        date = "2026-10-03"
        description = "Auto-generated CustomStyle detection rule"
        framework = "Style_Change_Framework"

    strings:
        $str_0 = "powershell -enc" ascii wide nocase
        $str_1 = "cmd.exe" ascii wide nocase

    condition:
        any of ($str_*)
}
