import formal
from formal.examples import main



class CompositeFormPage(main.FormExamplePage):
    
    title = 'Composite fields'
    description = 'Form containing composite fields'
    
    def form_example(self, ctx):

        # Create the form
        form = formal.Form()

        # Add a required name where the family name is required but the first
        # name is optional.
        form.add(formal.Field('name', formal.Composite([
            ('family', formal.String(required=True)),
            ('first', formal.String())],
            required=True)))

        # Add an optional temperature field where, once entered, both values
        # must be entered.
        form.add(formal.Field('temperature', formal.Composite([
            ('temperature', formal.Integer(required=True)),
            ('units', formal.String(required=True))])))

        # Add a required height field where both values are also required.
        form.add(formal.Field('height', formal.Composite([
            ('feet', formal.Integer(required=True)),
            ('inches', formal.Integer(required=True))],
            required=True)))

        # Add the submit action
        form.addAction(self.submitted)

        return form

    def submitted(self, ctx, form, data):
        print form, data
