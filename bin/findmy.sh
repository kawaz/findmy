#!/usr/local/bin/bash
mypath=$(realpath -e "$0")
[[ $0 == "$mypath" ]] || exec "$mypath" "$@"
cd "$(dirname "$0")/.." || exit 1

preprocess() {
  if direnv status | grep -q "^No .envrc loaded"; then
    [[ -z $SELF_EXECUTE ]] && SELF_EXECUTE=1 exec direnv exec . "$mypath" "$@"
    exit 1
  fi

  if ! type -P tv >/dev/null; then
    brew install uzimaru0000/tap/tv
  fi
  if ! type -P poetry >/dev/null; then
    brew install poetry
    poetry install
  fi
}

findmy() {
  python findmy.py "$@"
}

list_json() {
  local q='select(.name|match($name))|{id,deviceDiscoveryId,deviceClass,deviceDisplayName,name,fmlyShare,isLocating,activationLocked,batteryStatus,batteryLevel,lowPowerMode,"latlng":"\(.location.latitude),\(.location.longitude)","locTs":.location.timeStamp,"locDelay":((now*1000-(.location.timeStamp//0))/1000),"locType":.location.positionType,"locAc":.location.horizontalAccuracy}|(.+{locUrl:(if .locAc then "https://www.google.com/maps/?q=@\(.latlng)" else null end)})'
  python findmy.py device list | jq -rc --arg name "$1" "${q:-.}"
}

list_table() {
  list_json "$@" | jq -s 'map(del(.id)|del(.deviceDiscoveryId)|del(.latlng))' | tv -s batteryLevel
}


play() {
  local devices=$(list_json "$1" | jq -cr '{id,deviceDisplayName,name,batteryLevel,locUrl}')
  jq . <<< "$devices"
  if [[ $(wc -l <<< "$devices") == 1 ]]; then
    python findmy.py device play_sound "$(jq -r .id <<< "$devices")"
  fi
}

usage() {
  echo "Usage:"
  echo "  $0 list [NAME]     list devices in table"
  echo "  $0 json [NAME]     list devices in json"
  echo "  $0 play NAME       play sound"
  exit
}

preprocess
case $1 in
  list) list_table "$2";;
  json) list_json "$2";;
  play) play "$2";;
  *) usage
esac
