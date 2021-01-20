#/bin/bash

echo "Testing against: $MY_FINANCES_HOST"

echo "Creating ini file for test..."
cat <<EOF >> integration_tests/test_config.ini
[DEFAULT]
MY_FINANCES_HOST=$MY_FINANCES_HOST
EOF
echo "Done!"

echo "Starting pytest..."
pytest integration_tests
