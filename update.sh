todays_date=$(date +'%m/%d/%Y')
# echo Updating for $todays_date
python3 progress.py
git add --a
git commit -m "Update for $todays_date"
git push