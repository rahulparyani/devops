#!/bin/bash

days=+30
mins=+50

dest=/data/logs/logarchivetemp/
destarchive=/data/logs/logarchive/


servername=`hostname`
currentdatetime=`date +%F-%H-%M-%S`


echo $servername
echo $currentdatetime

logbackupforother(){

        dest1=$dest
        if ( [ ! -d $dest1 ] ); then
            echo "dest1 is not found"
            sudo mkdir $dest1
            sudo chown -R centos:centos $dest1
        fi
        dest1+=$servername-$appname-$currentdatetime
        echo "dest1 is $dest1"

        if ( [ ! -d $dest1 ] ); then
            echo "dest is not found"
            sudo mkdir $dest1
        fi

        cd $src
        echo copying logs files form $src $dest1 
        sudo find . -type f -mtime +3 -exec sudo rsync --remove-source-files --exclude '*.hprof' --exclude 'server.log' --exclude 'wrapper.log' --exclude 'wrapper.log.lck' --exclude 'task.log' --exclude 'htmlformservice.log' --exclude 'bidwinner.log' --exclude 'download.log' --exclude 'gc-*.log.*.current' --exclude 'gcLog.log.*.current' --exclude 'gcLog.log.0.current' --exclude 'adoddleShopApp.log' --exclude 'formdesigner.log' --exclude 'marketplace.log' --exclude 'messaging.log' --exclude 'notification.log' -av {} $dest1  \;

        if ( [ ! -d $destarchive ] ); then
            echo "not found $destarchive"
            sudo mkdir $destarchive
            sudo chown -R centos:centos $destarchive
        fi

        logcount=( $( ls $dest1 | wc -l) )
        echo log count is $logcount  

        if (( $logcount > 0 )); then
            destarchive1=$destarchive
            destarchive1+=$servername-$appname-$currentdatetime
            destarchive1+='.zip'
            echo "Creating zip" 
            zip -r $destarchive1 $dest1 > /dev/null
            echo "zip Created" 
            echo "#################################################################################################" 
        fi
}

logbackup(){
    echo "logbackup started"
    folderList=( $( find $src -maxdepth 0 -type d ) )

    if (( ${#folderList[@]} != 0 )); then
        len=${#folderList[@]}
        for (( i=0; i<$len; i++ ))
            do
                path=${folderList[$i]}
                appname=`basename "$path"`
                path+=$logpathpattern

                if ( ! [ ! -d $path ] ); then
                    echo " path found $path"
                    dest1=$dest
                    if ( [ ! -d $dest1 ] ); then
                        echo "dest1 is not found"
                        sudo mkdir $dest1
                        sudo chown -R centos:centos $dest1
                    fi

                    dest1+=$servername-$appname-$currentdatetime
                    echo "dest1 is $dest1"

                    if ( [ ! -d $dest1 ] ); then
                        echo "dest is not found"
                        sudo mkdir $dest1
                    fi
                    echo copying logs files from $path to $dest1 
                    sudo rsync --remove-source-files --exclude '*.hprof' --exclude 'server.log' --exclude 'wrapper.log' --exclude 'wrapper.log.lck' --exclude 'task.log' --exclude 'htmlformservice.log' --exclude 'bidwinner.log' --exclude 'download.log' --exclude 'gc-*.log.*.current' --exclude 'gcLog.log.*.current' --exclude 'gcLog.log.0.current' --exclude 'adoddleShopApp.log' --exclude 'formdesigner.log' --exclude 'marketplace.log' --exclude 'messaging.log' --exclude 'notification.log' --exclude 'application.log' -av $path/ $dest1  
                    #sudo rsync --exclude '*.hprof' --exclude 'server.log' --exclude 'wrapper.log' --exclude 'wrapper.log.lck' --exclude 'task.log' --exclude 'htmlformservice.log' --exclude 'bidwinner.log' --exclude 'download.log' --exclude 'gc-*.log.*.current' --exclude 'gcLog.log.*.current' --exclude 'gcLog.log.0.current' --exclude 'adoddleShopApp.log' --exclude 'formdesigner.log' --exclude 'marketplace.log' --exclude 'messaging.log' --exclude 'notification.log' -av $path/*.* $dest1  

                    if ( [ ! -d $destarchive ] ); then
                        echo "not found $destarchive"
                        sudo mkdir $destarchive
                        sudo chown -R centos:centos $destarchive
                    fi

                    logcount=( $( ls $dest1 | wc -l) )
                    echo log count is $logcount  
                    if (( $logcount > 0 )); then
                        destarchive1=$destarchive
                        destarchive1+=$servername-$appname-$currentdatetime
                        destarchive1+='.zip'
                        #echo "Creating zip" 
                        zip -r $destarchive1 $dest1  > /dev/null
                        #echo "zip Created" 
                        echo "#################################################################################################" 
                    fi
                fi
            done
    fi

}

##############################################################################

src=/data/asitemicroapps/*
if ( [ -d $src ] ); then
logpathpattern='/war/log'
logbackup
echo "script over microapps"
fi

##############################################################################

src=/data/wildfly-9.0.1.Final/*
if ( [ -d $src ] ); then
logpathpattern='/log'
logbackup
echo "script over wildfly"
fi

##############################################################################

src=/data/tomcat/*
if ( [ -d $src ] ); then
logpathpattern='/log'
logbackup
echo "script over tomcat"
fi

##############################################################################

src=/data/asitemicroapps/formdesignerui/logs/
if ( [ -d $src ] ); then
appname=formdesignerui
logbackupforother
echo "script over formdesignerui"
fi

##############################################################################

src=/data/asitemicroapps/branding/logs/
if ( [ -d $src ] ); then
appname=branding
logbackupforother
echo "Script over branding"
fi

##############################################################################

#Added on 17-12-2021 Reason : TECHOPS 6006
#Added by : Kunal Parekh

src=/data/logs/apache/
if ( [ -d $src ] ); then
appname=apache
logbackupforother
echo "Script over for apache"
fi

##############################################################################

echo "Older than $mins mintues"
#find $destarchive/*.zip -type f -mmin $mins
echo "Older than $days days"
#find $destarchive/*.zip -type f -mtime $days

#find $destarchive/*.zip -type f -mtime $days -exec rm {} \;
sudo rm -fr $dest

echo "script over"
