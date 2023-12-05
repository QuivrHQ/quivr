* Configure the Upstream Repository:

If you haven't already configured the upstream repository (the original repository you forked), you need to add it to your local clone. Replace upstream with the name you want to give to the remote and original_repository_URL with the URL of the original repository:

`git remote add upstream https://github.com/StanGirard/quivr`

* Fetch Upstream Changes:

Fetch the changes from the upstream repository:

`git fetch upstream`

* Check Out Your Local Branch:

Check out the branch in your fork where you want to incorporate the changes from the upstream repository. This is often the master or main branch:

`git checkout main`

* Merge Upstream Changes:

Merge the changes from the upstream repository’s main branch into your local branch:

`git merge upstream/main`

* Resolve Conflicts:

After attempting to merge, you may run into conflicts. Git will indicate which files have conflicts. Open these files in a text editor and look for the conflict markers (<<<<<<<, =======, >>>>>>>). Manually resolve the conflicts by choosing which changes to keep.

* Commit the Resolutions:

Once you have resolved the conflicts, add and commit these changes:

```bash
git add .
git commit -m "Resolved conflicts"
```

* Push to Your Fork:

Push the changes to your fork on GitHub:

`git push origin main`

* Pull Request (Optional):
If you intend to contribute your changes back to the original repository, create a pull request from your fork to the upstream repository.
