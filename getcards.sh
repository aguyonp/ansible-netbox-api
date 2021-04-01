#/usr/bin/bash

#Get physical cards name

#cards=$(find /sys/class/net -type l -not -lname '*virtual*' -printf '%f\n')

#Get physical cards and virtual cards
cards=$(find /sys/class/net -type l -printf '%f\n')

#printf '{"networks": {'
for card in $cards
do
        #Test if ip a command exist
        err=$(command -v ip a &> /dev/null ; echo $?)

        if [ $err -eq  0 ]
        then
                #If ip a exist
                ip=$(ip a | grep -wns $card -A 1 | sed -n 's/.* inet \([^ ]*\).*/\1/p')
        else
                #If ip a dont exist, use ifconfig
                ip=$(ifconfig | grep -wns $card -A 1 | sed -n 's/.* inet \([^ ]*\).*/\1/p')
        fi

        if [ -z "$ip" ]
        then
                ip="No ip address"
        fi
        echo $card $ip
done
# printf '}}'
# echo ""
# networks+="127.0.10.10"
# for x in "${networks[@]}"
# do
#         echo $x | sed 's|.*|"&"|'
# done | jq -s '.'