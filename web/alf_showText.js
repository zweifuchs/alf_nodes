import { app } from "../../../scripts/app.js";

app.registerExtension({
  name: "ALF.ShowText",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "ALF_ShowText") {
      nodeType.prototype.onExecuted = function (message) {
        console.log("xALFTEXTx onExecuted called with message:", message);
      };
    }
  },
});
