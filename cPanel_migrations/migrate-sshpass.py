#!/usr/bin/python
# --------------------------------------------------------------------
# Import libraries
# --------------------------------------------------------------------
import os
# --------------------------------------------------------------------
# User Input
# --------------------------------------------------------------------

# Site Manager Info
sm_path = raw_input('What is the full path from root to the public_html folder?\n') 
server_sm = raw_input('What is the Site Manager Server?\n')
sm_user = raw_input('What is the Site Manager username?\n')
sm_pass = raw_input('What is the Site Manager password?\n')

# Chi Info
server_chi = raw_input('What is the Chi server?\n')
chi_user = raw_input('What is the Chi username?\n')
chi_pass = raw_input('What is the Chi Password?\n')

# --------------------------------------------------------------------
# Global Variables
# --------------------------------------------------------------------

make_folders = 'cd / && mkdir /migration && mkdir /migration/websites && mkdir /migration/databases && mkdir /migration/ftp'
move_content = 'cp -rv /var/www/html /migration/websites'
move_databases = 'for x in $(mysql -BNe \'show databases\' | grep -v \"^mysql$\|information_schema\|^test$\");do mysqldump $x > /migration/databases/$x.sql;done'
move_ftp = 'cp -r /ftp/pub /migration/ftp'
tar = 'tar cvzf /migration.tar.gz /migration'

# --------------------------------------------------------------------
# Tar & Move
# --------------------------------------------------------------------

print("\nThe migration has started and can take a few hours. \nPlease reply to the client and let them know. \nYou will still need to check their account for problem applications also!")

#This connects to the account.
os.system("""('sshpass -p') + str(" ") + sm_pass + str(" ") + str("ssh") + str("-oStrictHostKeyChecking=no -l") + sm_user + "@" + server_sm + time.sleep(5) + str("&&") + chi_user + str("@") + server_chi + ":~" +
    \"cd / && mkdir /migration && mkdir /migration/websites && mkdir /migration/databases &&  mkdir /migration/ftp && cp -r /ftp/pub /migration/ftp && cp -rv /var/www/html /migration/websites" +
    \"for x in $(mysql -BNe \'show databases\' | grep -v \"^mysql$\|information_schema\|^test$\");" + "do" + "mysqldump $x > /migration/databases/$x.sql;done" + "tar cvzf /migration.tar.gz /migration" +
    \"wget http://cmerkley.whsites.net/apps/rsync && mv rsync /usr/bin' + \"rsync -rup --rsync-path=\"mkdir -p ~/migration/websites/ && mkdir -p ~/migration/databases/ && rsync" + sm_path + chi_user + "@" + server_chi + ":~/migration.tar.gz""")
