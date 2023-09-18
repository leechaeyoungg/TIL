# Git

## 최초설정

커밋에 기록되는 사용자 정보

```bash
git config --global user.name "John Doe"
git config --global user.email johndoe@example.com

```

## 로컬 명령어
- `git init`
- ./  ../  .git/ ->숨김처리돼서 보이지 않는 폴더
    - `.git` : git repository를 생성하는 명령어

- `.` ->현재 폴더


- `git add <file name>`
    - `working directory` 에서 `staging area`로 추가하는 과정
    - 일반적으로 모든 파일,폴더를 한번에 추가하기 위해
    아래의 명령어로 작성
    - `git add .`


- git commit -m "first commit" (`git commit`)
    - `staging area`에 올라간 파일들의 스냅샷을 찍어 `.git directory`에 저장
    - 일반적으로 -m옵션을 넣어서 커밋메세지를 추가
    - `git commit -m "message"'

    
git remote add origin https://github.com/leechaeyoungg/TIL.git
됐는지 확인(origin 떠야 완료된 것)
git remote
origin




## 원격저장소
- `git remote`
    - 원격저장소 주소를 관리하기 위한 명령어
    - `git remote add origin <url>`


- git push
    - 원격저장소에 로컬 코드를 업로드 하기 위한 명령어
    -`git push <remote> <branch(master)>`
    

    