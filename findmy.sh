#!/usr/local/bin/bash
mypath=$(realpath -e "$0")
[[ $0 == "$mypath" ]] || exec "$mypath" "$@"
cd "$(dirname "$0")" || exit 1

if direnv status | grep -q "^No .envrc loaded"; then
    [[ -z $SELF_EXECUTE ]] && SELF_EXECUTE=1 exec direnv exec . "$mypath" "$@"
    exit 1
fi

if [[ -z $1 ]]; then
    python findmy.py device list | jq -r '{deviceClass,fmlyShare,isLocating,activationLocked,batteryStatus,batteryLevel,name,lowPowerMode,"latlng":"\(.location.latitude),\(.location.longitude)","locTs":.location.timeStamp,"locDelay":((now*1000-(.location.timeStamp//0))/1000),"locType":.location.positionType,deviceDiscoveryId,"locAc":.location.horizontalAccuracy}' |jq -s|tv -s batteryLevel
    exit
fi

devices=$(python findmy.py device list | jq -rc --arg name "$1" 'select(.name|match($name))|{id,deviceDisplayName,name,batteryLevel,"loc":"https://www.google.com/maps/?q=@\(.location.latitude),\(.location.longitude)"}')
jq . <<< "$devices"

if [[ $(wc -l <<< "$devices") == 1 ]]; then
    if [[ $2 == play ]]; then
        python findmy.py device play_sound "$(jq -r .id <<< "$devices")"
    fi
fi