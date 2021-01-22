#/bin/bash

echo "Testing against: $MY_FINANCES_HOST"

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' $MY_FINANCES_HOST/login)" != "200" ]]; do
    sleep 2
    echo "Waiting for my_finances to be available..."
done

INI_FILE=integration_tests/test_config.ini

echo "Creating ini file for test..."
rm -f $INI_FILE
cat <<EOF >> $INI_FILE
[DEFAULT]
MY_FINANCES_HOST=$MY_FINANCES_HOST
EOF
echo "Done!"

echo "Starting pytest..."
pytest integration_tests
