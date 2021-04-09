su - postgres -c "psql -c \"DROP DATABASE dev_database;\""
PGUSER=postgres PGPASSWORD=testing heroku pg:pull postgresql-metric-93781 dev_database -a cs3240-a-18