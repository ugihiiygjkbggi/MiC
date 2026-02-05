# MiC
Welcome members of OMG lab.
You can use Git Bash to upload file, below are some instructions.



## A. 第一次把 repo 抓下來並上傳檔案
```bash
cd "C:\NYCU 2527\OMG Lab\git" # 在本機建一個總資料夾
git clone <REPO_URL>  # <REPO_URL>輸入我們這個repo的URL，成功後應該會在總資料夾底下出現 MiC 的資料夾
cd "<repo-folder>"    # <repo-folder>就會是MiC的路徑

git status
git remote -v

# 放檔案到這個資料夾底下（可先測試）

mkdir test
echo hello > test/hello.txt

git add .
git commit -m "add files"
git push -u origin main
```


## B. 之後日常更新（每次要上傳新檔/改檔）
```bash
cd "<repo-folder>"

git pull --rebase
git status

git add .
git commit -m "update"
git push
```

## C. 刪除檔案/資料夾並同步到遠端
```bash
git rm test/hello.txt
# 或刪整個資料夾
git rm -r test

git commit -m "remove test"
git push
```

## D. 遠端網址/分支確認
```bash
git remote -v
git branch
```

## E. 只改「這個 repo」之後 commit 顯示的作者（不等於登入帳號）
```bash
git config user.name "Your Name"
git config user.email "your@email.com"
```
