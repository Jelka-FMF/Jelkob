document.addEventListener('DOMContentLoaded', () => {
    const simulationContainer = document.getElementById('simulation-container');
    if (simulationContainer) {
        // Render the detailed ASCII Christmas tree
        simulationContainer.innerHTML = `
            <pre id="simulation-tree">
              <span class="tree-leaf">          .     .  .      +     .      .          .</span>
              <span class="tree-leaf">         .       .      .     #       .           .</span>
              <span class="tree-leaf">            .      .         ###            .      .      .</span>
              <span class="tree-leaf">          .      .   "#:. .:##"##:. .:#"  .      .</span>
              <span class="tree-leaf">              .      . "####"###"####"  .</span>
              <span class="tree-leaf">           .     "#:.    .:#"###"#:.    .:#"  .        .</span>
              <span class="tree-leaf">      .             "#########"#########"        .        .</span>
              <span class="tree-leaf">            .    "#:.  "####"###"####"  .:#"   .       .</span>
              <span class="tree-leaf">         .     .  "#######""##"##""#######"                  .</span>
              <span class="tree-leaf">                    ."##"#####"#####"##"           .      .</span>
              <span class="tree-leaf">           .   "#:..  .:##"###"###"##:. .. .:#"     .</span>
              <span class="tree-leaf">          .      "#######"##"#####"##"#######"      .     .</span>
              <span class="tree-leaf">         .    .     "#####""#######""#####"    .      .</span>
              <span class="tree-leaf">               .     "       000      "    .     .</span>
              <span class="tree-leaf">           .         .   .   000     .        .       .</span>
              <span class="tree-leaf">    .. .. ..................O000O........................ ...</span>
              <span class="tree-trunk">                            </span>
            </pre>
            <p id="simulation-text">Click the tree to light it up!</p>
        `;

        const treeElement = document.getElementById('simulation-tree');
        const leafElements = treeElement.getElementsByClassName('tree-leaf');
        const textElement = document.getElementById('simulation-text');
        textElement.style.cursor = 'pointer';

        textElement.addEventListener('click', () => {
            let colorIndex = 0;
            const colors = ['green', 'red', 'gold', 'blue', 'purple'];

            const intervalId = setInterval(() => {
                // Change the color of the leaf elements only
                Array.from(leafElements).forEach(leaf => {
                    leaf.style.color = colors[colorIndex];
                });
                colorIndex = (colorIndex + 1) % colors.length;
            }, 500);

            // Stop the animation after 10 seconds
            setTimeout(() => {
                clearInterval(intervalId);
                Array.from(leafElements).forEach(leaf => {
                    leaf.style.color = 'green'; // Reset to default leaf color
                });
            }, 10000);
        });
    }
});
