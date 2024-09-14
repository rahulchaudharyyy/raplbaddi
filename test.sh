PULL_OUTPUT=$(git pull origin production)

if [[ $PULL_OUTPUT == *"Already up to date."* ]]; then
    echo "Already up-to-date, no need to migrate or restart."
else
    echo "Changes detected, running bench migrate and restart."
    bench migrate
    bench restart
fi

