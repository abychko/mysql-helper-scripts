# pfs-adjustments

Converts CSV file (may be taken from ethalon MySQL server) to SQL or CNF file. The main idea behind it - counters are VERY expensive, disable unused or even disable them all and enable only required.

## configuration steps:
```
pfs-adjustments --infile expdata.csv --format cnf
```
upload resulting perfschema.cnf to /etc/mysql/conf.d and set in my.cnf
```
!include /etc/mysql/conf.d/perfschema.cnf
```

if you have no access to filesystem, then execute as follows:
```
pfs-adjustments --infile expdata.csv --format sql
```
and feed resulting SQL file as
```
mysql -u${USER} -p${PASSWORD} -h${HOST} < perfschema.sql
```

### for what?
we've got a final gain as 136k QPS (mostly inserts) using PFS + configuration tuning. general tuning is strongly advised to be performed before any actions related to PFS.

