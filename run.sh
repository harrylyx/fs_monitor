cd /root/fs_monitor
python3 remind.py
python3 save.py
cd /root/HomeAccount
git pull
git add .
git commit -m "update price"
git push