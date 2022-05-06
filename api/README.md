# Journal Checker Tool API

This software provides the API for the Journal Checker Tool.

Plan S aims for full and immediate Open Access to peer-reviewed scholarly publications from research funded by public 
and private grants. [cOAlition S](https://www.coalition-s.org/) is the coalition of research funding and performing 
organisations that have committed to implementing Plan S. The goal of cOAlition S is to accelerate the transition to a 
scholarly publishing system that is characterised by immediate, free online access to, and largely unrestricted use and 
re-use (full Open Access) of scholarly publications.

The Journal Checker Tool enables researchers to check whether they can comply with their funders Plan S aligned OA 
policy based on the combination of journal, funder(s) and the institution(s) affiliated with the research to be 
published. The tool currently only identifies routes to open access compliance for Plan S aligned policies.

This is a [cOAlition S](https://www.coalition-s.org/) project.


## Installation

Install meteor framework:

curl https://install.meteor.com/ | sh

Clone this repo, and go into the repo folder

Create a settings.json file, and put a JSON object in it. You'll need keys 
called "name" and "version", which can be anything - "noddy" is usually the name 
because this app was built on a library called noddy. You can also set "dev" to 
true for a dev installation (this mainly affects the index names where your data 
will be stored). Also add a key called "log", pointing to an object containing a 
key called "level", which you can set to "debug".

Then add a key called "es" pointing to an object containing "urL" and "index". 
URL must be the URL of your elasticsearch index, which is required. NOTE also 
this only works with old ES 1.4.x at the moment - it is highly recommended to 
upgrade this codebase, the server/elasticsearch.coffee file, to work with a 
newer version of ES (it should be straightforward). You can include 
username:password@ in your URL if your ES instance requires them. "index" should 
be the default index name to use, the best option here again is "noddy".

(NOTE: an old version of ES is currently required, but installing one is beyond 
the scope of these installation docs - you'll need to investigate that online, 
or upgrade the code to use a newer ES and then follow their simple instructions 
on their website. Alternatively there are providers of ready-made ES instances 
where you can pay as you go, and even get access to free tiers for 
non-production use.)

A "mail" key is also required in settings.json, pointing to an object containing 
"domain" and "apikey". These should be your mailgun domain and apikey - see 
mailgun.com for an account, it is required if you want the system to send emails.

Last for settings.json, add a key called "service" pointing to an object 
containing "jct", which should itself point to an object containing "doaj", 
which should point to an object containing "apikey". This must be your DOAJ API 
key for retrieving the DOAJ in progress applications (talk to doaj.org team 
about getting a special API key for this, as it is a unique feature for JCT).

Run the install command to set up dependencies:

meteor npm install

Finally, to start the app, run:

MONGO_URL="http://nowhere" && meteor --port 3002 --settings settings.json

We use port 3002 for dev and 3333 for live by default. We don't use MongoDB but 
it's a default for Meteor, so we set the MONGO_URL to nowhere. Start it in a 
screen if you want to leave it running, or install and use pm2 if you prefer 
for running it in production.

You can also control how much memory it can take up, such as: 

export NODE_OPTIONS='--max-old-space-size=3072' && export MONGO_URL="http://nowhere" && meteor --port 3333 --settings settings.json


## About the code

This codebase was originally written on a library called Noddy, which uses 
Meteor, but the code has now been ported to be standalone (although still 
requires Meteor).

/server/lib contains the necessary parts from Noddy, stripped 
down to only what JCT needs, to keep it simple and easy to maintain. If future 
JCT development requires features such as auth, check out the old Noddy codebase 
which has many more advanced capabilities (although note it is being deprecated 
- it would still work, but won't be receiving new improvements). aestivus.coffee 
contains the main structure of the API, and api.coffee instantiates the API. 
collection.coffee handles data collections, and it stores and interacts with 
them using elasticsearch.coffee.

/server/service/jct contains the code of the JCT app itself. It's all in one 
file called api.coffee (there's another called scripts.coffee which was just 
used for initial prototyping and data bootstrapping). api.coffee defines the 
API routes and the methods that should be called when each of them is used.

Code is written in Coffeescript which gets converted into javascript. You can 
read more about coffeescript at coffeescript.org. It's a bit obsolete now 
because node has improved over the years, taking on a lot of the feature that 
coffeescript provided. However, coffeescript is still neater to write, so it's 
just a preference. Any future development can be written in .js files instead 
if preferred, and merging them all together is automatically handled anyway.

If you develop the code and add a new dependency, use 
"meteor npm install --save ..." to add it to the package list, and then when 
you deploy the code, "meteor npm install" will need to be run again too.


# About Meteor

Much more info is of course available at meteor.com, but generally Meteor is not 
very well utilised in this project any more. Like coffeescript, it was handy to 
use before modern node.js improved. However it is still a good and well 
supported framework, so using it causes no harm. Whilst many of the features it 
was designed for are not used because JCT is only an API with a separate static 
UI and we don't use MongoDB, the build, run, and management features of meteor 
are still used.

"meteor list" lists all the installed meteor packages

"meteor add ..." can be used to add a meteor package

"meteor remove ..." will remove one

"meteor npm install --save ..." can be used to install and manage node packages

"meteor npm uninstall ..." will uninstall a node package.

Meteor also handles dependencies, and the version of Node to use, internally.


## Installing on a virtual machine (optional)

A 4GB 2vCPU DO machine with the latest Ubuntu server works fine.
(2GB would run the app but it needs up to 4GB for some of the data uploads.)

adduser --gecos "" USERNAME

cd /home/USERNAME

mkdir /home/USERNAME/.ssh

chown USERNAME:USERNAME /home/USERNAME/.ssh

chmod 700 /home/USERNAME/.ssh

mv /root/.ssh/authorized_keys .ssh/

(or make the authorized_keys file and put the necessary key in it)

chown USERNAME:USERNAME .ssh/authorized_keys

chmod 600 /home/USERNAME/.ssh/authorized_keys

adduser USERNAME sudo

export VISUAL=vim

visudo

(in visudo add this line: USERNAME ALL=(ALL) NOPASSWD: ALL)

apt-get update

apt-get -q -y install ntp g++ build-essential screen htop git-core curl

dpkg-reconfigure tzdata

(set to Europe/London)

dpkg-reconfigure --priority=low unattended-upgrades

vim /etc/ssh/sshd_config

(uncomment PubkeyAuthentication yes, change PermitRootLogin to no, ensure PasswordAuthentication is no)

service ssh restart

ufw allow 22

ufw allow 80

ufw allow 443

ufw enable

(if your Elasticsearch machine/cluster requires specific IP addresses to be 
given access, then run the necessary commands on your ES gateway machine, e.g.)

sudo ufw allow in on eth1 from MACHINEINTERNALIP to any port 9200

You will also need to setup nginx and certbot - there are nginx configs provided 
in the repo. Symlink these into /etc/nginx/sites-enabled and restart nginx. 
Follow further instructions online if you need help with nginx, or need help 
with certbot. A command such as the following should get your certbot setup, 
but note you may need to comment out the SSL sections of the nginx config first, 
as nginx won't accept them before the certs exist.

sudo certbot certonly -d YOURDOMAINNAME.COM

Now follow the normal Installation instructions above. By default we run dev on 
port 3002 and production on port 3333, and the nginx configs expect that, but 
can be customised to your preference.

## Updating the service with funder-db submodule

This will update the branch checked out and pull the latest funder-db submodule, meteor will restart the application for us.

```bash
git pull && git submodule update --init --recursive
```
