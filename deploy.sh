#!/bin/bash

cd "$(dirname "$0")"

if [[ -r "${HOME}/.karma_manager_deploy" ]]; then
    source "${HOME}/.karma_manager_deploy"
fi

if [[ -z "${KM_USERHOST}" ]]; then
    echo "Set KM_USERHOST to user@hostname for deployment"
    exit 1
fi

if [[ -z "${KM_WEBDIR}" ]]; then
    echo "Set KM_WEBDIR to directory on remote host where website lives"
    exit 1
fi
    
if [[ "$1" == "beta" ]]; then 
    rsync -av web/* ${KM_USERHOST}:${KM_WEBDIR}/beta/.
elif [[ "$1" == "prod" ]]; then
    rsync -av web/* ${KM_USERHOST}:${KM_WEBDIR}/.
else
    echo "Usage: $0 { prod | beta }" 
fi
