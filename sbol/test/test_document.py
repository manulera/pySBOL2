import locale
import os
import unittest
# Needed for setHomespace and maybe Config and some other things
from sbol.document import *
import sbol

MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
TEST_LOCATION = os.path.join(MODULE_LOCATION, 'resources', 'crispr_example.xml')


class TestDocument(unittest.TestCase):

    def test_empty_len0(self):
        doc = sbol.Document()
        # print(doc)
        self.assertEqual(0, len(doc), "Length of document should be 0")

    def test_addGetTopLevel_uri(self):
        doc = sbol.Document()
        # Tutorial doesn't drop final forward slash, but this isn't right.
        setHomespace('http://sbols.org/CRISPR_Example')
        Config.setOption('sbol_compliant_uris', True)
        Config.setOption('sbol_typed_uris', False)
        crispr_template = ModuleDefinition('CRISPR_Template')
        cas9 = ComponentDefinition('Cas9', BIOPAX_PROTEIN)
        doc.addModuleDefinition(crispr_template)
        doc.addComponentDefinition(cas9)

        # Note: tutorial has 1.0.0 instead of 1 but this doesn't work
        crispr_template_2 = doc.getModuleDefinition('http://sbols.org/CRISPR_Example/CRISPR_Template/1')
        cas9_2 = doc.getComponentDefinition('http://sbols.org/CRISPR_Example/Cas9/1')
        self.assertEqual(crispr_template, crispr_template_2)
        self.assertEqual(cas9, cas9_2)

    def test_addGetTopLevel_displayId(self):
        doc = sbol.Document()
        setHomespace('http://sbols.org/CRISPR_Example')
        Config.setOption('sbol_compliant_uris', True)
        Config.setOption('sbol_typed_uris', False)
        crispr_template = ModuleDefinition('CRISPR_Template')
        cas9 = ComponentDefinition('Cas9', BIOPAX_PROTEIN)
        doc.addModuleDefinition(crispr_template)
        doc.addComponentDefinition(cas9)

        crispr_template_2 = doc.moduleDefinitions['CRISPR_Template']
        cas9_2 = doc.componentDefinitions['Cas9']
        self.assertEqual(crispr_template, crispr_template_2)
        self.assertEqual(cas9, cas9_2)

    def test_addGetTopLevel_indexing(self):
        doc = sbol.Document()
        # Tutorial doesn't drop final forward slash, but this isn't right.
        setHomespace('http://sbols.org/CRISPR_Example')
        Config.setOption('sbol_compliant_uris', True)
        Config.setOption('sbol_typed_uris', False)
        crispr_template = ModuleDefinition('CRISPR_Template')
        cas9 = ComponentDefinition('Cas9', BIOPAX_PROTEIN)
        doc.addModuleDefinition(crispr_template)
        doc.addComponentDefinition(cas9)

        crispr_template_2 = doc.moduleDefinitions[0]
        cas9_2 = doc.componentDefinitions[0]
        self.assertEqual(crispr_template, crispr_template_2)
        self.assertEqual(cas9, cas9_2)

    def test_iteration(self):
        doc = sbol.Document()
        doc.read(TEST_LOCATION)
        i = 0
        for obj in doc:
            i += 1
            # print(obj)
        self.assertEqual(len(doc), 31)
        # print(doc)

    def test_identity(self):
        # The sbol:identity relation should not be written out when
        # serializing SBOL.
        doc = sbol.Document()
        doc.read(TEST_LOCATION)
        result = doc.writeString()
        self.assertNotIn('sbol:identity', result)

    def test_utf8_append(self):
        utf8_path = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL2', 'pICSL50014.xml')
        doc = sbol.Document()
        doc.append(utf8_path)

    def test_utf8_append_no_locale(self):
        # Test loading a utf-8 SBOL file without LANG set. This was a
        # bug at one time, and only shows itself when LANG is unset.
        # Here we simulate that by temporarily setting the locale to
        # the generic 'C' locale.
        utf8_path = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL2', 'pICSL50014.xml')
        loc = locale.getlocale()
        try:
            locale.setlocale(locale.LC_ALL, 'C')
            doc = sbol.Document()
            doc.append(utf8_path)
        finally:
            locale.setlocale(locale.LC_ALL, loc)

    def test_utf8_read(self):
        utf8_path = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL2', 'pICSL50014.xml')
        doc = sbol.Document()
        doc.read(utf8_path)

    def test_utf8_read_no_locale(self):
        # Test loading a utf-8 SBOL file without LANG set. This was a
        # bug at one time, and only shows itself when LANG is unset.
        # Here we simulate that by temporarily setting the locale to
        # the generic 'C' locale.
        utf8_path = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL2', 'pICSL50014.xml')
        loc = locale.getlocale()
        try:
            locale.setlocale(locale.LC_ALL, 'C')
            doc = sbol.Document()
            doc.read(utf8_path)
        finally:
            locale.setlocale(locale.LC_ALL, loc)


if __name__ == '__main__':
    unittest.main()
