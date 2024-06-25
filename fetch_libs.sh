#!/bin/bash

cd "$(dirname $0)"

mkdir -p web/lib
cd web/lib
for x in https://ajax.googleapis.com/ajax/libs/angularjs/1.6.9/angular.min.js https://github.com/mbenford/ngTagsInput/releases/download/v3.2.0/ng-tags-input.min.zip; 
do
   wget ${x}
done

unzip ng-tags-input.min.zip
rm ng-tags-input.min.zip
