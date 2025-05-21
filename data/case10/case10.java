public synchronized void channelsProgress(String id, double p) {
    ProgressNode pn = progressNodes.get(id);
    boolean ins = false;
    if (pn == null) {
      pn = new ProgressNode();
      progressNodes.put(id, pn);
      ins = true;
    }
    if (!filesNodeInTree) {
      model.insertNodeInto(filesNode, rootNode, 0);
      filesNodeInTree = true;
      ins = true;
    }
    pn.setProgress(p);
    if (ins) {
      model.insertNodeInto(pn, filesNode, 0);
      dataTree.expandPath(new TreePath(filesNode.getPath()));
    }
    if (p == 1) {
      progressNodes.remove(id);
      filesNode.remove(pn);
    }
    dataTree.repaint();
}