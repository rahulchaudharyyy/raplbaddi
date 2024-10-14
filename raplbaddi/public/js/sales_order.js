frappe.ui.form.on("Sales Order", {
  refresh: function (frm) {
    frm.events.queries(frm);
  },
  queries(frm) {
    frm.set_query("billing_rule", function () {
      return {
        query: "raplbaddi.controllers.queries.billing_rule",
        filters: {
          applicable_for: ["in", ["Selling", "Both"]],
        },
      };
    });
  },
});