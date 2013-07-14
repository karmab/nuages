nuages repository
================


    This web portal running on django allows you to provide self-service  on top  of your :
    -virtualproviders(rhev/ovirt/vsphere)
    -physical(ilo)
    -foreman
    -cobbler/satellite
    -VMs can be created,stopped,started,deleted and their console access (ovirt/rhev only)
    -VMS get created based on predefined profiles ( with a given virtualprovider and optional foremanprovider and cobblerprovider, and vm details such as disksize ( 2 disks supported), net interfaces ( 4 nets supported ) ,...)
    -Authentication can use remote ldap providers

What s that name?
------------
    well it s a django project with a feel of cloud, and django reinhardt most famous song is "nuages", which means cloud in french...Get it :) ?


Profile
------------
    A profile is a combination of :
    -a virtual provider (rhev/ovirt/vsphere)
    -virtual machine information ( datacenter,cluster,memory, guestid, number ov vcpus, number of interfaces( up to 4) ,logical networks, size and format of the disks,...
    -a physical provider containing ilo credentials to access ILO through ssh
    -an optional foreman provider where machine will be created, along with puppetclasses and puppetparameters. The List of hostgroups will automatically be fetched when selecting a profile with foreman support
    -an optional cobbler provider where the machine will be created, along with cobbler parameters
    -iso support. The list of available isos from the virtualprovider will automatically be fetched when selecting a profile with iso support
     
Type
------------
    When creating a machine,you can specify a type based on the following ones:
    -Apache
    -Oracle
    -Rac
    -Weblogic
    -Cluster
    you ll get and additional dialog box displayed with specific parameters that will be passed as cobbler parameters to your cobbler provider when creating the machine



Requisites
------------

    a DB (postgresql is what i used but sqlite3 is another simpler option)
    ovirt-engine-sdk package (only if you will connect to ovirt/rhev)
    jython and vsphere api libraries ( only if you will connect to vcenter/esx)
    paramiko ( to connect to ILO through ssh)
    gateone (from https://github.com/liftoff/GateOne ) (only if you want to connect to your physical machines ssh-ing to their ilo and then running vsp )
    optionally apache server  with mod_wsgi

Ovirt SDK Installation
--------

    from epel:
    yum -y install ovirt-engine-sdk


VMware VI (vSphere) Java API Installation
------------

        1. Download latest version of  http://vijava.sourceforge.net/

        2. Unzip archive with unzip vijava$version.zip

        3. Move jar resultantes to lib/ext of your java install (ext/lib en fedora)
        for instance, with default jre on ubuntu:

        JAVA_HOME=/usr/lib/jvm/java-6-openjdk/jre
        sudo cp dom4j-1.6.1.jar $JAVA_HOME/ext/lib
        sudo cp vijava$version.jar $JAVA_HOME/ext/lib

        Or for a 64 bits fedora16 :
        JAVA_HOME=/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.3.x86_64/jre
        sudo cp dom4j-1.6.1.jar $JAVA_HOME/ext/lib/ext
        sudo cp vijava$version.jar $JAVA_HOME/lib/ext


Basic Postgresql setup (Optional)
---------
    
    note: you can skip that  if you plan to use sqlite
	install postgresql-server for your distribution For instance, on rhel6.4, from epel

    yum -y install postgresql-server python-psycopg2
    
    initialize and start DB, creating a user called nuages with a db called nuages)
        
    service postgresql initdb ; /etc/init.d/postgresql start  ; su - postgres ; createuser nuages -P -d -R -S ; createdb -O nuages nuages

    allow DB TCP connections. edit /var/lib/pgsql/data/pg_hba.conf so that it contains for instance
    local   all         all                               ident
    host   all         all     127.0.0.1/32                md5

    service postgresql restart


App Installation 
---------
     
    clone the repo ( or get an archive):
    
    git clone https://github.com/karmab/nuages.git

	install django and south for your distribution (and paramiko). For instance, on rhel6.4, from epel

    yum -y install Django14 Django-south python-paramiko

    if you ll use a postgresql DB
     
    yum -y install python-psycopg2 


    edit $NUAGES_PATH/nuages/settings.py to reflect correct DB information.You can either use postgresql as i do or simply set sqlite3 ( in that case, change name of the sqlite file, for instance to nuages.sqlite)

    create django tables.create superuser when asked for:

    python manage.py syncdb 

    create south stuff 

    python manage.py schemamigration portal --initial

    python manage.py migrate portal --fake

    launch integrated web server:

    python manage.py runserver YOUR_IP:YOUR_PORT


Apache Integration 
------------------    
    install apache and mod_wsgi
    
    uncompress the tar where you plan to serve it from apache ( ex: /var/www/nuages )
    
    edit $NUAGES_PATH/nuages/settings.py to reflect correct DB credentials
    
    edit $NUAGES_PATH/django.wsgi to reflect correct location  (replace /var/www/nuages if necessary)                                                       
    
    create a virtual host conf for apache. you can use the nuages.conf.apache  sample provided
	
    restart apache

 
Usage
---------
	
     use the superuser you created as part of the django deployment...
     access the /admin page to :
		*create local users
    	*create ldap user providers 
		*create virtualproviders
		*create physicalproviders
		*create foremanproviders
		*create cobblerproviders
		*create default ( otherwise the yourvms console tab wont work! )
		*create profiles
	
     drop the CA certificates of your rhev/ovirt virtualproviders and ldapproviders in the nuages dir

     access the /nuages page to :
     		*access the storage tab and browse your virtualproviders so storage information gets automatically created
     
     you can then begin creating vms or manage existing ones from the allvms tabs

 
Screenshots
---------
![ScreenShot](https://raw.github.com/karmab/nuages/master/screenshots/nuages1.png)
![ScreenShot](https://raw.github.com/karmab/nuages/master/screenshots/nuages2.png)
![ScreenShot](https://raw.github.com/karmab/nuages/master/screenshots/nuages3.png)
![ScreenShot](https://raw.github.com/karmab/nuages/master/screenshots/nuages4.png)

Problems?                                                                                                                                                                      
---------

Drop me a mail at karimboumedhel@gmail.com !

Mac Fly!!!

karmab
