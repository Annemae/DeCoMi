private boolean uptodate(ResourceCollection src, ResourceCollection target) {
    org.apache.tools.ant.types.resources.selectors.Date datesel
        = new org.apache.tools.ant.types.resources.selectors.Date();
    datesel.setMillis(System.currentTimeMillis());
    datesel.setWhen(TimeComparison.AFTER);
    // don't whine because a file has changed during the last
    // second (or whatever our current granularity may be)
    datesel.setGranularity(0);
    logFuture(targets, datesel);

    NonExistent missingTargets = new NonExistent(targets);
    int neTargets = missingTargets.size();
    if (neTargets > 0) {
        log(neTargets + " nonexistent targets", Project.MSG_VERBOSE);
        logMissing(missingTargets, "target");
        return false;
    }
    Resource oldestTarget = getOldest(targets);
    logWithModificationTime(oldestTarget, "oldest target file");

    logFuture(sources, datesel);

    NonExistent missingSources = new NonExistent(sources);
    int neSources = missingSources.size();
    if (neSources > 0) {
        log(neSources + " nonexistent sources", Project.MSG_VERBOSE);
        logMissing(missingSources, "source");
        return false;
    }
    Resource newestSource = getNewest(sources);
    logWithModificationTime(newestSource, "newest source");
    return oldestTarget.getLastModified() >= newestSource.getLastModified();
}