# -*- coding: utf-8 -*-
"""
/***************************************************************************
                              -------------------
        begin                : 23/03/17
        git sha              : :%H$
        copyright            : (C) 2017 by Germán Carrillo (BSF-Swissphoto)
        email                : gcarrillo@linuxmail.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QObject

ILI2PG_VERSION = '3.10.6'
ILI2PG_URL = 'http://www.eisenhutinformatik.ch/interlis/ili2pg/ili2pg-{}.zip'.format(ILI2PG_VERSION)

class BaseConfiguration(object):
    def __init__(self):
        self.custom_model_directories_enabled = False
        self.custom_model_directories = ''
        self.java_path = ''
        self.logfile_path = ''
        self.debugging_enabled = False

    def save(self, settings):
        settings.setValue('CustomModelDirectoriesEnabled', self.custom_model_directories_enabled)
        settings.setValue('CustomModelDirectories', self.custom_model_directories)
        settings.setValue('JavaPath', self.java_path)
        settings.setValue('LogfilePath', self.logfile_path)
        settings.setValue('DebuggingEnabled', self.debugging_enabled)

    def restore(self, settings):
        self.custom_model_directories_enabled = settings.value('CustomModelDirectoriesEnabled', False, bool)
        self.custom_model_directories = settings.value('CustomModelDirectories', '', str)
        self.java_path = settings.value('JavaPath', '', str)
        self.debugging_enabled = settings.value('DebuggingEnabled', False, bool)
        self.logfile_path = settings.value('LogfilePath', '', str)

    def to_ili2db_args(self, export_modeldir=True):
        args = []
        if export_modeldir:
            if self.custom_model_directories_enabled and self.custom_model_directories:
                args += ['--modeldir', self.custom_model_directories]
        args += ['--trace']
        if self.logfile_path:
            args += ['--log', self.logfile_path]
        return args

    @property
    def model_directories(self):
        dirs = list()
        if self.custom_model_directories_enabled and self.custom_model_directories:
            dirs = self.custom_model_directories.split(';')
        else:
            dirs = [
                '%ILI_FROM_DB',
                '%XTF_DIR',
                'http://models.interlis.ch/',
                '%JAR_DIR'
            ]
        return dirs

class ImportConfiguration(object):
    def __init__(self):
        self.ilifile = ''
        self.inheritance = 'smart1'
        self.epsg = 21781  # Default EPSG code in ili2pg
        self.host = ''
        self.user = ''
        self.database = ''
        self.schema = ''
        self.password = ''
        self.port = ''
        self.ilimodels = ''

        self.base_configuration = BaseConfiguration()

    @property
    def uri(self):
        uri = []
        uri += ['dbname={}'.format(self.database)]
        uri += ['user={}'.format(self.user)]
        if self.password:
            uri += ['password={}'.format(self.password)]
        uri += ['host={}'.format(self.host)]
        if self.port:
            uri += ['port={}'.format(self.port)]

        return ' '.join(uri)


class ExportConfiguration(object):
    def __init__(self):
        self.xtffile = ''
        self.host = ''
        self.user = ''
        self.database = ''
        self.schema = ''
        self.password = ''
        self.port = ''
        self.ilimodels = ''

        self.base_configuration = BaseConfiguration()


class ImportDataConfiguration(object):
    def __init__(self):
        self.xtffile = ''
        self.host = ''
        self.user = ''
        self.database = ''
        self.schema = ''
        self.password = ''
        self.port = ''
        self.ilimodels = ''
        self.delete_data = False

        self.base_configuration = BaseConfiguration()


class JavaNotFoundError(FileNotFoundError):
    pass
