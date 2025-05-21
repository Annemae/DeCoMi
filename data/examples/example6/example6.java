public static void openWinConfigFileDialog() {
  JFileChooser chooser = new JFileChooser(); 
  chooser.setFileFilter(new FileNameExtensionFilter("WIN Config (.config)", "config")); 
  chooser.addChoosableFileFilter(new FileNameExtensionFilter("Text File (.txt)", "txt"));
  chooser.setCurrentDirectory(new File(swarmConfig.lastPath));
  chooser.setFileSelectionMode(JFileChooser.FILES_ONLY); 
  chooser.setMultiSelectionEnabled(false); 
  chooser.setDialogTitle("Select WIN configuration file..."); 
  if (WinDataFile.configFile != null) { 
    chooser.setSelectedFile(WinDataFile.configFile);
  }
  int result = chooser.showOpenDialog(applicationFrame);
  if (result == JFileChooser.APPROVE_OPTION) { 
    File f = chooser.getSelectedFile();
    SwarmConfig.getInstance().lastPath = f.getParent(); 
    WinDataFile.configFile = f; 
  }
}