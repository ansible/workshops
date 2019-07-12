# Contribute

We take pull requests!  

## Create a fork!
Create a fork on your own Github project (or your personal space)

[Github Documentation on Forking a repo](https://help.github.com/articles/fork-a-repo/)

## Stay in Sync
It is important to know how to keep your fork in sync with the upstream Workshops project.

### Configuring Your Remotes
Configure `ansible/workshops` as your upstream so you can stay in sync

```bash
git remote add upstream https://github.com/ansible/workshops.git
```

### Rebasing Your Branch
Three step process

```bash
git pull --rebase upstream master
```

```bash
git status
```

### Updating your Pull Request
```bash
git push --force
```

More info on docs.ansible.com: [Rebasing a Pull Request](http://docs.ansible.com/ansible/latest/dev_guide/developing_rebasing.html)

## Create a pull requests

Make sure you are not behind (in sync) and then submit a PR to the Ansible Workshops.  
[Read the Pull Request Documentation on Github.com](https://help.github.com/articles/creating-a-pull-request/)

Just because you submit a PR, doesn't mean that it will get accepted.  Right now the QA process is manual for Workshops, so provide detailed directions on

 - WHY? Why did you make the change?
 - WHO? Who is this for?  If this is something for a limited audience it might not make sense for all users.
 - BEST PRACTICE?  Is this the "best" way to do this?  Link to documentation or examples where the way you solved your issue or improved the Ansible Workshops is the best practice for teaching or building workshops.

Being more descriptive is better, and has a higher change of getting merged upstream.  Communication is key!  Just b/c the PR doesn't get accepted right away doesn't mean it is not a good idea. Ansible Workshops have to balance many different types of users.  Thank you for contributing!

# Notes April 3rd, 2019

Load this into your ~/.bashrc or ~/.oh-my-zsh/oh-my-zsh.sh

```
pullupstream () {
  if [[ -z "$1" ]]
  then
    printf "Error: must specify a branch name (e.g. - master, devel)\n"
  else
    pullup_startbranch=$(printf "%s" "$(grep '\*' <(git branch) | sed s/\*.//)")
    git checkout "$1"
    git fetch upstream
    git merge "upstream/$1"
    git push origin "$1"
    git checkout "${pullup_startbranch}"
  fi
}
```

Check out your local devel branch from your fork
```bash
git checkout devel
```

Run the pullupstream command

```bash
pullupstream
```

Check out your feature branch
```bash
git checkout ipvsean/april3
```

rebase your branch based off your local devel branch after you confirm your devel branch is 1:1 with upstream

```bash
git pull --rebase origin master
```

1) Fork
2) Clone devel
2a)git remote add upstream https://github.com/ansible/workshops.git
origin    https://github.com/gdykeman/workshops (fetch)
origin    https://github.com/gdykeman/workshops (push)
upstream    https://github.com/ansible/workshops.git (fetch)
upstream    https://github.com/ansible/workshops.git (push)
3) git checkout <branch name>
4) Make changes
5) push branch into origin
6) PR to upstream/devel
7) git fetch upstream
8) checkout devel
9) git merge upstream/devel
10) git push


# Going Further
The following links will be helpful if you want to contribute code to the Ansible Workshops project, or any Ansible project:
- [Ansible Committer Guidelines](http://docs.ansible.com/ansible/latest/committer_guidelines.html)
- [Learning Git](https://git-scm.com/book/en/v2)
