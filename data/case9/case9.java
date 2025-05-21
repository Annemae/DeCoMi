private static NotationSettings initializeDefaultSettings() {
    NotationSettings settings = new NotationSettings();
    settings.parent = null;
    settings.setNotationLanguage(Notation.DEFAULT_NOTATION);
    settings.setFullyHandleStereotypes(false);
    settings.setShowAssociationNames(true);
    settings.setShowInitialValues(false);
    settings.setShowMultiplicities(false);
    settings.setShowPaths(false);
    settings.setShowProperties(false);
    settings.setShowSingularMultiplicities(true);
    settings.setShowTypes(true);
    settings.setShowVisibilities(false);
    settings.setUseGuillemets(false);
    return settings;
}