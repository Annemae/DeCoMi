/** {@inheritDoc}. */
public void executeTargets(Project project, String[] targetNames)
    throws BuildException {
    BuildException thrownException = null;
    for (String targetName : targetNames) {
        try {
            project.executeTarget(targetName);
        } catch (BuildException ex) {
            if (project.isKeepGoingMode()) {
                thrownException = ex;
            } else {
                throw ex;
            }
        }
    }
    if (thrownException != null) {
        throw thrownException;
    }
}