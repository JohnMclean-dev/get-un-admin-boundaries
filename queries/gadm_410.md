# GADM 4.1 Schema

## Administrative Boundary Levels

| Level | Name | Alternate Name | Native/Local Name | ISO Code | HASC Code | CC Code | Type | English Type | Valid From |
|-------|------|----------------|-------------------|----------|-----------|---------|------|--------------|------------|
| `gid_0` | `name_0` | `varname_0` | — | — | — | — | — | — | — |
| `gid_1` | `name_1` | `varname_1` | `nl_name_1` | `iso_1` | `hasc_1` | `cc_1` | `type_1` | `engtype_1` | `validfr_1` |
| `gid_2` | `name_2` | `varname_2` | `nl_name_2` | — | `hasc_2` | `cc_2` | `type_2` | `engtype_2` | `validfr_2` |
| `gid_3` | `name_3` | `varname_3` | `nl_name_3` | — | `hasc_3` | `cc_3` | `type_3` | `engtype_3` | `validfr_3` |
| `gid_4` | `name_4` | `varname_4` | — | — | — | `cc_4` | `type_4` | `engtype_4` | `validfr_4` |
| `gid_5` | `name_5` | — | — | — | — | `cc_5` | `type_5` | `engtype_5` | — |

## Additional Columns

| Column Group | Columns |
|-------------|---------|
| Identifiers | `fid`, `uid` |
| Sovereignty & Governance | `governedby`, `sovereign`, `disputedby` |
| Geographic Classification | `region`, `varregion`, `country`, `continent`, `subcont` |
| Geometry | `geom` |

## Hierarchy

```text
gid_0 → Country
gid_1 → Admin Level 1
gid_2 → Admin Level 2
gid_3 → Admin Level 3
gid_4 → Admin Level 4
gid_5 → Admin Level 5
```