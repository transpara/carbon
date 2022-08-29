# Carbon Demo



```bash
February 3, 2022 - Inselbuch
now uses tstore-api for writes
containerized

September 10, 2021 - Inselbuch
initial version (tsdb)
```

## Run Docker Container from Transpara Dockerhub Image


```bash
docker run --rm -d \
    --pid host \
    --network transpara \
    --name carbon \
    --hostname carbon \
    -e host_name=`hostname` \
    -e PYTHONUNBUFFERED=1 \
    -e promURL="http://tstore-api:80/api/v1/write" \
    transpara/carbon
```


## Build from source


```bash
cd /transpara
git clone https://github.com/transpara/carbon
./build.sh
./rundocker.sh
```

## Simulation Tags



Tags are simulated using the tagfile.txt file. This is a comma-separated text file with no header row. Each line contains a tagname and a typical value. The simulation will randomly deliver values that surround the typical value.

```bash
Total (Mtoe),23.9
Total (TJ),1004052
Total Consum,205.8
Total Cooling,14402.6
Total Ete Consum,23145
Total Hazardous,51816
Total Location,1.43
Total Market,2.285
```

Note: Tagnames are represented as labels within promscale so the following transformations are applied to text identifiers:

```bash
all characters are converted to lowercase
spaces are replaced with underscores
forward slashes are replaced with underscores
additional transforms may be required, this function is not exhaustive
```

### Linking the tagfile to the container

The tagfile is copied into the container within the Dockerfile. This requires additional steps when modifying the tagfile.

To avoid that, it is possible to have the external tagfile appear within the container filesystem by adding the following to the docker run command:


-v `pwd`tagFile.text:/tagFile.txt:ro \


## Verify proper operation

If successfully running, new values should arrive approximately every minute. This can be verified with the following query on the tstore database.


```bash
transpara=# select time,value,val(tagname_id),val(hostname_id) from carbon order by time desc limit 20;
            time            |        value         |      val       |   val
----------------------------+----------------------+----------------+---------
 2022-02-03 23:26:06.338+00 |   1.6669247399822016 | Nat Gas        | ubuntu3
 2022-02-03 23:26:06.305+00 |   0.3686791346113515 | MV             | ubuntu3
 2022-02-03 23:26:06.273+00 |    73095.56168196916 | Mining (Ete)   | ubuntu3
 2022-02-03 23:26:06.242+00 |    48.37758378147799 | Mining         | ubuntu3
 2022-02-03 23:26:06.211+00 |    28.48856508742273 | MEX S3 Em      | ubuntu3
 2022-02-03 23:26:06.173+00 |    5.836839082082886 | MEX S2 Em      | ubuntu3
 2022-02-03 23:26:06.139+00 | 0.029301611721401662 | MEX S1 Em      | ubuntu3
 2022-02-03 23:26:06.102+00 |    9.593702660525892 | Management     | ubuntu3
 2022-02-03 23:26:06.07+00  |    61.66712180319964 | LV/MV          | ubuntu3
 2022-02-03 23:26:06.038+00 |    84.11078786524456 | LV             | ubuntu3
 2022-02-03 23:26:06.006+00 |   3.6347526329788153 | Lubricant      | ubuntu3
 2022-02-03 23:26:05.972+00 |    83.15426782878507 | Lime           | ubuntu3
 2022-02-03 23:26:05.94+00  |   1338.8733364633413 | Lignite (TJ)   | ubuntu3
 2022-02-03 23:26:05.905+00 |   102.19346185930549 | Lignite (Raw)  | ubuntu3
 2022-02-03 23:26:05.863+00 |  0.03121551102175648 | Lignite (Mtoe) | ubuntu3
 2022-02-03 23:26:05.829+00 |   0.0964122018101958 | Lignite        | ubuntu3
 2022-02-03 23:26:05.798+00 |    353138.6313745994 | Landfill (NH)  | ubuntu3
 2022-02-03 23:26:05.765+00 |    9809.714342058187 | Landfill (H)   | ubuntu3
 2022-02-03 23:26:05.734+00 |    6465.100552603084 | Jap S3 Em      | ubuntu3
 2022-02-03 23:26:05.703+00 |    6504.523532869673 | Jap S2 Em      | ubuntu3
```

