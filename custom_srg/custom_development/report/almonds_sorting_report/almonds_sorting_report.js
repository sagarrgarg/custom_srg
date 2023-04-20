// Copyright (c) 2023, SRG and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Almonds Sorting Report"] = {
	"filters": [
		{
            fieldname: 'batch_no',
            label: __('Batch No'),
            fieldtype: "Link",
			options: "Batch",
			reqd:1,
        },
	]
};
