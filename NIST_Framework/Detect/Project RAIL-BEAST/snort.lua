------------------------------------------------------------
-- RAIL‑BEAST Minimal Compatible Snort 3 Configuration
------------------------------------------------------------

ips =
{
    enable_builtin_rules = true,


}

references = default_references
classifications = default_classifications

file_id =
{
    rules_file = 'file_magic.rules'
}

alert_fast =
{
    file = true,
}

logging =
{
    log_dir = '/var/log/snort',
}
