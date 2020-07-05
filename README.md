# digispider (Digikala Spider)

Digikala Spider is a project aimed at crawling `Digikala` seller website to see how many new orders are submitted for example and send its information to target notification channel. 

### Installation Guide

Digispider is an installable package. In order to install the package run the below command:

```bash
python3 setup.py install
```

By installing the package, you will have a command at your disposal. The method is called
`ds_fetch` which is used to fetch a resource like `Digikala` orders.

Method usage is as follow:

```bash
ds_fetch --operation TargetResource
```

For instance:

```bash
ds_fetch --operation orders
```

Before that you need to set an environment variable called `DS_CONFIG` to your json configuration 
path like `/etc/ds_config.json`:

```bash
export DS_CONFIG=/etc/ds_config.json
```

Please have a look at the configuration sample file called `config.sample.json` in order to know what is required configurations.

### MongoDB installation

Digi spider needs MongoDB in order to be able to run and store latest orders. To install mongodb in one go you can use below docker command:

```
docker run --name digimongo --restart always -e MONGO_INITDB_ROOT_USERNAME=YOUR_USERNAME -e MONGO_INITDB_ROOT_PASSWORD=YOUR_PASS -v /data/mongo:/data/db -p 27017:27017 -d mongo
```

Just note that you need to have `/data/mongo` directory in your host machine.

If you want to run the script periodically you can use crontab:

```
*/10 * * * * env DS_CONFIG=/etc/digi-config.json /usr/local/bin/ds_fetch --operation orders >> /var/log/digi-spider.log 2>&1
```

Here we put log information in `/var/log/digi-spider.log`
