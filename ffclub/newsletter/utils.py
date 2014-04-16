# -*- coding: utf-8 -*-
from .models import *
import os
from ffclub.settings import NEWSLETTER_ASSETS_URL


def build_meta_params(all_metadata=None, admin=False):
    params = {}

    if all_metadata:
        tags = {}
        for meta in all_metadata:
            if isinstance(meta, MetaString) and meta.name.endswith('-tag'):
                key = meta.name[:-4]
                if key not in tags:
                    tags[key] = {}
                tags[key][meta.index] = meta.value

        for meta in all_metadata:
            val = meta.value
            if isinstance(meta, MetaDatetime):
                val = val.strftime('%Y/%m/%d')
            elif isinstance(meta, MetaFile):
                key = meta.name[:meta.name.rfind('-')]
                val = NEWSLETTER_ASSETS_URL + ('' if admin or key not in tags else '/tagged/') + os.path.basename(val.file.name)
            if meta.index == 0:
                params[meta.name] = val
            else:
                if meta.name not in params:
                    params[meta.name] = {}
                params[meta.name][meta.index] = val

    if 'article-thumb' not in params:
        params['article-thumb'] = {}
    if 'article-link' not in params:
        params['article-link'] = {}
    if 'article-tag' not in params:
        params['article-tag'] = {}
    if 'article-title' not in params:
        params['article-title'] = {}
    if 'article-desc' not in params:
        params['article-desc'] = {}
    if 'quiz-answer' not in params:
        params['quiz-answer'] = {}

    return params

