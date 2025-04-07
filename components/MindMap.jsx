import React, { useEffect, useRef } from 'react';

const MindMap = ({ data }) => {
  const containerRef = useRef(null);
  
  // Parse text-based mind map into structured data
  const parseMindMap = (text) => {
    const lines = text.split('\n');
    const mindMapData = { central: '', branches: [] };
    let currentBranch = null;
    
    lines.forEach(line => {
      if (line.startsWith('Central Topic:')) {
        mindMapData.central = line.replace('Central Topic:', '').trim();
      } else if (line.match(/^Branch \d+:/)) {
        const branchName = line.replace(/^Branch \d+:/, '').trim();
        currentBranch = { name: branchName, subBranches: [] };
        mindMapData.branches.push(currentBranch);
      } else if (line.match(/^\s+Sub-branch \d+\.\d+:/) && currentBranch) {
        const subBranchName = line.replace(/^\s+Sub-branch \d+\.\d+:/, '').trim();
        currentBranch.subBranches.push({ name: subBranchName });
      }
    });
    
    return mindMapData;
  };
  
  useEffect(() => {
    if (!containerRef.current) return;
    
    const mindMapData = typeof data === 'string' ? parseMindMap(data) : data;
    if (!mindMapData.central) return;
    
    // Clear previous content
    containerRef.current.innerHTML = '';
    
    // Create mind map container
    const mindMapElement = document.createElement('div');
    mindMapElement.className = 'flex flex-col items-center';
    
    // Create central node
    const centralNode = document.createElement('div');
    centralNode.className = 'p-3 bg-indigo-600 text-white rounded-lg font-medium mb-6 max-w-xs text-center';
    centralNode.textContent = mindMapData.central;
    mindMapElement.appendChild(centralNode);
    
    // Create branches container
    const branchesContainer = document.createElement('div');
    branchesContainer.className = 'flex flex-wrap justify-center gap-4 w-full';
    
    // Create branches
    mindMapData.branches.forEach(branch => {
      const branchElement = document.createElement('div');
      branchElement.className = 'flex flex-col items-center max-w-xs';
      
      // Create branch node
      const branchNode = document.createElement('div');
      branchNode.className = 'p-2 bg-indigo-400 text-white rounded-md font-medium mb-2 text-center';
      branchNode.textContent = branch.name;
      branchElement.appendChild(branchNode);
      
      // Create connection line from central to branch
      const connectionLine = document.createElement('div');
      connectionLine.className = 'w-px h-6 bg-gray-400 mb-1';
      
      // Insert connection line before branch node
      branchElement.insertBefore(connectionLine, branchNode);
      
      // Create sub-branches if any
      if (branch.subBranches && branch.subBranches.length > 0) {
        const subBranchesContainer = document.createElement('div');
        subBranchesContainer.className = 'flex flex-col items-center gap-1';
        
        branch.subBranches.forEach(subBranch => {
          // Create connection line from branch to sub-branch
          const subConnectionLine = document.createElement('div');
          subConnectionLine.className = 'w-px h-2 bg-gray-400';
          subBranchesContainer.appendChild(subConnectionLine);
          
          // Create sub-branch node
          const subBranchNode = document.createElement('div');
          subBranchNode.className = 'p-1 bg-indigo-200 text-indigo-800 rounded text-sm';
          subBranchNode.textContent = subBranch.name;
          subBranchesContainer.appendChild(subBranchNode);
        });
        
        branchElement.appendChild(subBranchesContainer);
      }
      
      branchesContainer.appendChild(branchElement);
    });
    
    mindMapElement.appendChild(branchesContainer);
    containerRef.current.appendChild(mindMapElement);
  }, [data]);
  
  return (
    <div 
      ref={containerRef} 
      className="min-h-[200px] border border-gray-200 rounded-lg p-4 bg-white overflow-auto"
      data-testid="mind-map-container"
    />
  );
};

export default MindMap;