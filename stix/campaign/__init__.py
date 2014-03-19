# Copyright (c) 2014, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

from datetime import datetime

import dateutil

import stix
import stix.bindings.campaign as campaign_binding
from stix.common import Confidence, InformationSource, StructuredText
from stix.common.related import GenericRelationshipList, RelatedCampaign, RelatedPackageRefs
from stix.data_marking import Marking
import stix.utils


class AssociatedCampaigns(GenericRelationshipList):
    _namespace = "http://stix.mitre.org/Campaign-1"
    _binding = campaign_binding
    _binding_class = campaign_binding.AssociatedCampaignsType
    _binding_var = "Associated_Campaign"
    _contained_type = RelatedCampaign
    _inner_name = "campaigns"


class Campaign(stix.Entity):
    _binding = campaign_binding
    _binding_class = _binding.CampaignType
    _namespace = "http://stix.mitre.org/Campaign-1"
    _version = "1.1"

    def __init__(self, id_=None, title=None, description=None):
        self.id_ = id_ or stix.utils.create_id("Campaign")
        self.idref = None
        self.timestamp = None
        self.version = self._version
        self.title = title
        self.description = description
        self.short_description = None
        # self.names = None
        # self.intended_effect = None
        # self.status = none
        # self.related_ttps = None
        # self.related_incidents = None
        # self.related_indicators = None
        # self.attribution = None
        self.associated_campaigns = AssociatedCampaigns()
        self.confidence = None
        # self.activity = None
        self.information_source = None
        self.handling = None
        self.related_packages = RelatedPackageRefs()

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if not value:
            self._timestamp = None
        elif isinstance(value, datetime):
            self._timestamp = value
        else:
            self._timestamp = dateutil.parser.parse(value)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value:
            if isinstance(value, StructuredText):
                self._description = value
            else:
                self._description = StructuredText(value=value)
        else:
            self._description = None

    def to_obj(self, return_obj=None):
        if not return_obj:
            return_obj = self._binding_class()

        return_obj.set_id(self.id_)
        return_obj.set_idref(self.idref)
        if self.timestamp:
            return_obj.set_timestamp(self.timestamp.isoformat())
        return_obj.set_version(self.version)
        return_obj.set_Title(self.title)
        if self.description:
            return_obj.set_Description(self.description.to_obj())
        if self.short_description:
            return_obj.set_Short_Description(self.short_description.to_obj())

        if self.associated_campaigns:
            return_obj.set_Associated_Campaigns(self.associated_campaigns.to_obj())
        if self.confidence:
            return_obj.set_Confidence(self.confidence.to_obj())

        if self.information_source:
            return_obj.set_Information_Source(self.information_source.to_obj())
        if self.handling:
            return_obj.set_Handling(self.handling.to_obj())
        if self.related_packages:
            return_obj.set_Related_Packages(self.related_packages.to_obj())

        return return_obj

    @classmethod
    def from_obj(cls, obj, return_obj=None):
        if not obj:
            return None

        if not return_obj:
            return_obj = cls()

        return_obj.id_ = obj.get_id()
        return_obj.idref = obj.get_idref()
        return_obj.timestamp = obj.get_timestamp()
        return_obj.version = obj.get_version() or cls._version
        return_obj.title = obj.get_Title()
        return_obj.description = StructuredText.from_obj(obj.get_Description())
        return_obj.short_description = \
                StructuredText.from_obj(obj.get_Short_Description())

        return_obj.associated_campaigns = \
                AssociatedCampaigns.from_obj(obj.get_Associated_Campaigns())
        return_obj.confidence = Confidence.from_obj(obj.get_Confidence())

        return_obj.information_source = \
                InformationSource.from_obj(obj.get_Information_Source())
        return_obj.handling = Marking.from_obj(obj.get_Handling())
        return_obj.related_packages = \
                RelatedPackageRefs.from_obj(obj.get_Related_Packages())

        return return_obj

    def to_dict(self):
        d = {}
        if self.id_:
            d['id'] = self.id_
        if self.idref:
            d['idref'] = self.idref
        if self.timestamp:
            d['timestamp'] = self.timestamp.isoformat()
        if self.version:
            d['version'] = self.version or self._version
        if self.title:
            d['title'] = self.title
        if self.description:
            d['description'] = self.description.to_dict()
        if self.short_description:
            d['short_description'] = self.short_description.to_dict()

        if self.associated_campaigns:
            d['associated_campaigns'] = self.associated_campaigns.to_dict()
        if self.confidence:
            d['confidence'] = self.confidence.to_dict()

        if self.information_source:
            d['information_source'] = self.information_source.to_dict()
        if self.handling:
            d['handling'] = self.handling.to_dict()
        if self.related_packages:
            d['related_packages'] = self.related_packages.to_dict()

        return d

    @classmethod
    def from_dict(cls, dict_repr, return_obj=None):
        if not dict_repr:
            return None

        if not return_obj:
            return_obj = cls()

        return_obj.id_ = dict_repr.get('id')
        return_obj.idref = dict_repr.get('idref')
        return_obj.timestamp = dict_repr.get('timestamp')
        return_obj.version = dict_repr.get('version', cls._version)
        return_obj.title = dict_repr.get('title')
        return_obj.description = \
                StructuredText.from_dict(dict_repr.get('description'))
        return_obj.short_description = \
                StructuredText.from_dict(dict_repr.get('short_description'))

        return_obj.associated_campaigns = \
                AssociatedCampaigns.from_dict(dict_repr.get('associated_campaigns'))
        return_obj.confidence = \
                Confidence.from_dict(dict_repr.get('confidence'))

        return_obj.information_source = \
                InformationSource.from_dict(dict_repr.get('information_source'))
        return_obj.handling = Marking.from_dict(dict_repr.get('handling'))
        return_obj.related_packages = \
                RelatedPackageRefs.from_dict(dict_repr.get('related_packages'))

        return return_obj
