#/bin/bash

while [[ "$(mysql --batch --skip-column-names -u $MYSQL_USER -p$MYSQL_PASSWORD -e "select 1" $MYSQL_DATABASE 2> /dev/null)" != "1" ]]; do
    echo "Waiting for mysql to standup..."
    sleep 2
done

echo "Starting my_finances..."
gunicorn -b 0.0.0.0:5000 app:app
