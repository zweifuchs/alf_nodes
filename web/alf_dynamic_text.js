import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
  name: "ALF.DynamicText",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "ALF_DynamicText") {
      console.log("DEBUG: Found ALF_DynamicText node");

      // Function to update widgets based on output
      function updateWidgets(output) {
        console.log("DEBUG: updateWidgets called with:", output);

        if (!Array.isArray(output) || output.length < 2) {
          console.log("DEBUG: Invalid output format");
          return;
        }

        const counterValue = output[1]; // Get counter from second output
        console.log("DEBUG: Counter value from output:", counterValue);

        if (this.widgets) {
          const counterWidget = this.widgets.find((w) => w.name === "counter");
          if (counterWidget) {
            console.log(
              "DEBUG: Found counter widget, updating to:",
              counterValue
            );
            counterWidget.value = counterValue;

            // Mark widget and canvas as needing update
            counterWidget.dirty = true;
            app.graph.setDirtyCanvas(true, false);
          }
        }

        // Update canvas size if needed
        requestAnimationFrame(() => {
          const sz = this.computeSize();
          if (sz[0] < this.size[0]) sz[0] = this.size[0];
          if (sz[1] < this.size[1]) sz[1] = this.size[1];
          this.onResize?.(sz);
          app.graph.setDirtyCanvas(true, false);
        });
      }

      // Add the update function to the node type
      nodeType.prototype.onNodeCreated = function () {
        console.log("DEBUG: Node created");
      };

      // Hook the update function into execution
      const onExecuted = nodeType.prototype.onExecutionStart;
      nodeType.onExecutionStart = function () {
        message = this;
        widgets = this.widgets;
        console.log(
          "DEBUG: onExecuted called with message:",
          message,
          "and widgets:",
          widgets
        );

        if (message?.output) {
          console.log("DEBUG: Calling updateWidgets with output");
          updateWidgets.call(this, message.output);
        }

        return onExecuted?.apply(this, arguments);
      };
    }
  },
});
