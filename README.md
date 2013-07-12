nuages repository
------------------------------

This web portal running on django allows you to provide self-service  on top  of your :
    virtualproviders(rhev/ovirt/vsphere)
    physical(ilo)
    foreman
    cobbler/satellite
VMs can be created,stopped,started,deleted and their console access (ovirt/rhev only)
VMS get created based on predefined profiles ( with a given virtualprovider and optional foremanprovider and cobblerprovider, and vm details such as disksize ( 2 disks supported), net interfaces ( 4 nets supported ) ,...)
Authentication can use remote ldap providers

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

    a DB (postgresql is what i used)
    apache server  with mod_wsgi
    ovirt-engine-sdk package (only if you will connect to ovirt/rhev)
    jython and vsphere api libraries ( only if you will connect to vcenter/esx)
    gateone (from https://github.com/liftoff/GateOne ) (only if you want to connect to your physical machines ssh-ing to their ilo and then running vsp )

VMware VI (vSphere) Java API Instalation
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




Contents
--------

    README                           this file
    nuages                           directory containing the app
                                                            

Installation 
---------
     
     uncompress the tar where you plan to serve it from apache ( ex: /var/www/nuages ). I ll call that NUAGES_PATH from now on 
	
     edit $NUAGES_PATH/django.wsgi to reflect correct location  (replace /var/www/nuages if necessary)                                                       

     create a virtual host conf for apache. you can use the nuages.conf.apache 

     create user and database, and needed tables for instance
        su - postgres
        createuser nuages -P -d -R -S
        createdb -O nuages nuages
        psql -U nuages -d nuages -f nuages.sql

     create an initial admin user
       TODO...
    
    edit $NUAGES_PATH/nuages/settings.py to reflect correct DB credentials

    restart apache

 
Usage
---------
	
     access the /admin page to :
		*create local users
    		*create ldap user providers 
		*create virtualproviders
		*create physicalproviders
		*create foremanproviders
		*create cobblerproviders
		*create default
		*create profiles
	
     drop the CA certificates of your rhev/ovirt virtualproviders and ldapproviders in the nuages dir

     access the /nuages page to :
     		*access the storage tab and browse your virtualproviders so storage information gets automatically created
     
     you can then begin creating vms or manage existing ones from the allvms tabs

                                                                                                                                                                               
Problems?                                                                                                                                                                      
---------

Drop me a mail at karimboumedhel@gmail.com !

Mac Fly!!!

karmab
