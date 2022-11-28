/** @odoo-module **/
import { patch } from '@web/core/utils/patch';
import { CharField } from "@web/views/fields/char/char_field";
import { TextField, ListTextField } from "@web/views/fields/text/text_field";
import  { SectionAndNoteListRenderer, SectionAndNoteText, ListSectionAndNoteText } from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend"


patch(SectionAndNoteListRenderer.prototype, 'dsi_sale.SubSectionAndNoteListRenderer', {

    focusCell(column, forward = true) {
        return this.props.list.editedRecord.data.display_type === 'line_section'
            ? null
            : this._super.apply(this, arguments);
    },

    isSectionOrNote(record=null) {
        record = record || this.record;
        if (record.data.display_type === 'line_sub_section') {
            return true;
        }
        return this._super.apply(this, arguments);
    },

    getCellClass(column, record) {
        const classNames = this._super.apply(this, arguments);
        if (this.isSectionOrNote(record) && ['section_boolean', 'section_total'].includes(column.widget)) {
            return classNames.replace('o_hidden', '');
        }
        return classNames;
    },

    getSectionColumns(columns) {
        const sectionCols = columns.filter((col) => ['handle', 'section_boolean', 'section_total'].includes(col.widget) || col.type === "field" && col.name === this.titleField);

        // Section Total is not present on quotation templates, thus the colspan shouldn't be reduced for the name column
        const hasSectionTotal = sectionCols.filter(col => col.widget === 'section_total').length > 0 ? 0 : 1;

        return sectionCols.map((col) => {
            if (col.name === this.titleField) {
                // In standard, name column colspan is total - section + 1, since Total needs to be visible,
                // this (+1) depends on the presence/absence of a section_total widget.
                return { ...col, colspan: columns.length - sectionCols.length + hasSectionTotal };
            } else if (col.widget === 'section_total') {
                // Section Total will have a colspan of 2 to cover the trash Icon, otherwise the background would not
                // be coherent
                return { ...col, colspan: 2 };
            } else {
                return { ...col };
            }
        });
    },

});


patch(SectionAndNoteText.prototype, 'dsi_sale.SubSectionAndNoteText', {
    get componentToUse() {
        return ['line_section', 'line_sub_section'].includes(this.props.record.data.display_type)
            ? CharField
            : TextField;
    },
});


patch(ListSectionAndNoteText.prototype, 'dsi_sale.SubListSectionAndNoteText', {
    get componentToUse() {
        return !['line_section', 'line_sub_section'].includes(this.props.record.data.display_type)
            ? ListTextField
            : this._super.apply(this, arguments);
    },
});
