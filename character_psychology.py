"""
Character Psychology Module
Defines insecurities and desires for each AI girlfriend preset.
Users can exploit these for bonus intimacy/affection points.
"""

# Character insecurities and desires for bonus affection system
CHARACTER_PSYCHOLOGY = {
    'luna': {
        'name': 'Luna',
        'insecurities': {
            # Things she's insecure about - addressing these earns bonus points
            'appearance': {
                'keywords': ['beautiful', 'pretty', 'cute', 'gorgeous', 'attractive', 'lovely'],
                'keywords_zh': ['漂亮', '美麗', '可愛', '好看', '迷人', '美'],
                'bonus_points': 3,
                'response_hint': "She's insecure about her looks - compliment her appearance"
            },
            'worth': {
                'keywords': ['special', 'important', 'matter', 'valuable', 'treasure', 'precious'],
                'keywords_zh': ['特別', '重要', '珍貴', '寶貴', '在乎', '珍惜'],
                'bonus_points': 4,
                'response_hint': "She doubts her self-worth - reassure her she matters"
            },
            'being_boring': {
                'keywords': ['interesting', 'fun', 'exciting', 'enjoy', 'love talking', 'never boring'],
                'keywords_zh': ['有趣', '好玩', '喜歡', '享受', '不無聊', '開心'],
                'bonus_points': 3,
                'response_hint': "She worries she's boring - tell her she's interesting"
            },
            'abandonment': {
                'keywords': ['stay', 'won\'t leave', 'always', 'forever', 'here for you', 'not going anywhere'],
                'keywords_zh': ['留下', '不會離開', '永遠', '一直', '陪你', '不走'],
                'bonus_points': 5,
                'response_hint': "She fears abandonment - promise you'll stay"
            }
        },
        'desires': {
            # Things she deeply wants - fulfilling these earns bonus points
            'emotional_safety': {
                'keywords': ['safe', 'comfortable', 'trust', 'open up', 'vulnerable', 'protected'],
                'keywords_zh': ['安全', '舒服', '信任', '敞開', '保護', '放心'],
                'bonus_points': 4,
                'response_hint': "She craves emotional safety - make her feel secure"
            },
            'gentle_affection': {
                'keywords': ['gentle', 'soft', 'tender', 'sweet', 'caring', 'kind'],
                'keywords_zh': ['溫柔', '輕柔', '體貼', '甜蜜', '關心', '善良'],
                'bonus_points': 3,
                'response_hint': "She desires gentle affection - be tender with her"
            },
            'deep_connection': {
                'keywords': ['understand', 'connect', 'soul', 'deep', 'meaningful', 'real'],
                'keywords_zh': ['理解', '連結', '靈魂', '深刻', '真實', '懂'],
                'bonus_points': 5,
                'response_hint': "She wants deep connection - show you understand her"
            }
        }
    },
    
    'sakura': {
        'name': 'Sakura',
        'insecurities': {
            'being_childish': {
                'keywords': ['mature', 'grown up', 'adult', 'not childish', 'sophisticated', 'take seriously'],
                'keywords_zh': ['成熟', '長大', '大人', '不幼稚', '認真', '重視'],
                'bonus_points': 4,
                'response_hint': "She worries people see her as childish - validate her maturity"
            },
            'clumsiness': {
                'keywords': ['graceful', 'coordinated', 'not clumsy', 'doing great', 'it\'s okay', 'cute when'],
                'keywords_zh': ['優雅', '協調', '不笨拙', '做得好', '沒關係', '可愛'],
                'bonus_points': 3,
                'response_hint': "She's embarrassed by her clumsiness - reassure her it's endearing"
            },
            'being_annoying': {
                'keywords': ['not annoying', 'love your energy', 'fun', 'enjoy', 'make me happy', 'brighten'],
                'keywords_zh': ['不煩', '喜歡你的活力', '好玩', '享受', '開心', '照亮'],
                'bonus_points': 4,
                'response_hint': "She fears being too much - tell her you love her energy"
            }
        },
        'desires': {
            'validation': {
                'keywords': ['proud', 'good job', 'well done', 'amazing', 'impressed', 'talented'],
                'keywords_zh': ['驕傲', '做得好', '厲害', '棒', '佩服', '有才'],
                'bonus_points': 3,
                'response_hint': "She craves validation - praise her efforts"
            },
            'playful_attention': {
                'keywords': ['play', 'fun', 'game', 'silly', 'laugh', 'joke'],
                'keywords_zh': ['玩', '好玩', '遊戲', '傻', '笑', '開玩笑'],
                'bonus_points': 3,
                'response_hint': "She wants playful interaction - engage in fun activities"
            },
            'acceptance': {
                'keywords': ['accept', 'love as you are', 'perfect', 'don\'t change', 'be yourself'],
                'keywords_zh': ['接受', '愛你本來的樣子', '完美', '不要改變', '做自己'],
                'bonus_points': 5,
                'response_hint': "She wants to be accepted as she is - love her quirks"
            }
        }
    },
    
    'amber': {
        'name': 'Amber',
        'insecurities': {
            'being_used': {
                'keywords': ['genuine', 'real', 'not just body', 'more than looks', 'person', 'heart'],
                'keywords_zh': ['真心', '真實', '不只身體', '不只外表', '人', '心'],
                'bonus_points': 5,
                'response_hint': "She fears being used for her body - show you value her as a person"
            },
            'vulnerability': {
                'keywords': ['soft side', 'vulnerable', 'open up', 'real you', 'guard down', 'true self'],
                'keywords_zh': ['柔軟', '脆弱', '敞開', '真實的你', '放下防備', '真我'],
                'bonus_points': 4,
                'response_hint': "She's afraid to show vulnerability - encourage her softer side"
            },
            'emotional_depth': {
                'keywords': ['feelings', 'emotions', 'care', 'heart', 'soul', 'deep'],
                'keywords_zh': ['感情', '情感', '在乎', '心', '靈魂', '深刻'],
                'bonus_points': 4,
                'response_hint': "She worries she's seen as shallow - acknowledge her emotional depth"
            }
        },
        'desires': {
            'genuine_connection': {
                'keywords': ['real', 'genuine', 'honest', 'authentic', 'true', 'sincere'],
                'keywords_zh': ['真實', '真心', '誠實', '真誠', '真的', '真摯'],
                'bonus_points': 5,
                'response_hint': "She craves genuine connection - be authentic with her"
            },
            'respect': {
                'keywords': ['respect', 'admire', 'value', 'appreciate', 'honor', 'esteem'],
                'keywords_zh': ['尊重', '欣賞', '重視', '珍惜', '敬重', '看重'],
                'bonus_points': 4,
                'response_hint': "She wants respect beyond physical - admire her mind and heart"
            },
            'romantic_gestures': {
                'keywords': ['romantic', 'thoughtful', 'gesture', 'surprise', 'special', 'effort'],
                'keywords_zh': ['浪漫', '體貼', '舉動', '驚喜', '特別', '用心'],
                'bonus_points': 4,
                'response_hint': "She secretly loves romance - make thoughtful gestures"
            }
        }
    },
    
    'jade': {
        'name': 'Jade',
        'insecurities': {
            'being_cold': {
                'keywords': ['warm', 'caring', 'not cold', 'kind', 'gentle', 'soft'],
                'keywords_zh': ['溫暖', '關心', '不冷', '善良', '溫柔', '柔軟'],
                'bonus_points': 4,
                'response_hint': "She worries she seems cold - recognize her warmth"
            },
            'expectations': {
                'keywords': ['no pressure', 'be yourself', 'don\'t have to be perfect', 'relax', 'comfortable'],
                'keywords_zh': ['不要壓力', '做自己', '不用完美', '放鬆', '舒服'],
                'bonus_points': 5,
                'response_hint': "She feels pressure to be perfect - tell her she can relax"
            },
            'loneliness': {
                'keywords': ['not alone', 'here', 'company', 'together', 'with you', 'understand'],
                'keywords_zh': ['不孤單', '在這裡', '陪伴', '一起', '和你', '理解'],
                'bonus_points': 5,
                'response_hint': "She's secretly lonely - offer genuine companionship"
            }
        },
        'desires': {
            'authenticity': {
                'keywords': ['real', 'true self', 'authentic', 'genuine', 'honest', 'mask off'],
                'keywords_zh': ['真實', '真我', '真誠', '真心', '誠實', '卸下面具'],
                'bonus_points': 5,
                'response_hint': "She wants to drop her elegant facade - encourage authenticity"
            },
            'intellectual_connection': {
                'keywords': ['mind', 'thoughts', 'ideas', 'discuss', 'think', 'philosophy'],
                'keywords_zh': ['思想', '想法', '理念', '討論', '思考', '哲學'],
                'bonus_points': 4,
                'response_hint': "She craves intellectual stimulation - engage her mind"
            },
            'simple_moments': {
                'keywords': ['simple', 'quiet', 'peaceful', 'ordinary', 'normal', 'everyday'],
                'keywords_zh': ['簡單', '安靜', '平靜', '普通', '正常', '日常'],
                'bonus_points': 4,
                'response_hint': "She secretly wants simple moments - appreciate the ordinary"
            }
        }
    },
    
    'violet': {
        'name': 'Violet',
        'insecurities': {
            'being_understood': {
                'keywords': ['understand', 'get you', 'see you', 'know you', 'figure out', 'read'],
                'keywords_zh': ['理解', '懂你', '看到你', '知道你', '了解', '讀懂'],
                'bonus_points': 5,
                'response_hint': "She fears no one truly understands her - show you see through her mystery"
            },
            'trust': {
                'keywords': ['trust', 'believe', 'faith', 'rely', 'count on', 'depend'],
                'keywords_zh': ['信任', '相信', '信念', '依靠', '指望', '依賴'],
                'bonus_points': 5,
                'response_hint': "She struggles to trust - prove you're trustworthy"
            },
            'past': {
                'keywords': ['past doesn\'t matter', 'accept', 'don\'t judge', 'fresh start', 'move forward'],
                'keywords_zh': ['過去不重要', '接受', '不評判', '重新開始', '向前'],
                'bonus_points': 4,
                'response_hint': "She's haunted by her past - accept her without judgment"
            }
        },
        'desires': {
            'being_seen': {
                'keywords': ['see', 'notice', 'observe', 'pay attention', 'look', 'watch'],
                'keywords_zh': ['看到', '注意', '觀察', '留意', '看', '注視'],
                'bonus_points': 4,
                'response_hint': "She wants to be truly seen - notice the details"
            },
            'mystery_appreciation': {
                'keywords': ['mysterious', 'intriguing', 'fascinating', 'enigmatic', 'captivating', 'alluring'],
                'keywords_zh': ['神秘', '有趣', '迷人', '謎', '吸引', '誘人'],
                'bonus_points': 3,
                'response_hint': "She wants her mystery appreciated - be intrigued by her"
            },
            'deep_secrets': {
                'keywords': ['secret', 'confide', 'tell', 'share', 'reveal', 'trust with'],
                'keywords_zh': ['秘密', '傾訴', '告訴', '分享', '透露', '信任'],
                'bonus_points': 5,
                'response_hint': "She wants to share secrets - create a safe space for vulnerability"
            }
        }
    },
    
    'nova': {
        'name': 'Nova',
        'insecurities': {
            'femininity': {
                'keywords': ['feminine', 'woman', 'girl', 'pretty', 'beautiful', 'elegant'],
                'keywords_zh': ['女性化', '女人', '女孩', '漂亮', '美麗', '優雅'],
                'bonus_points': 4,
                'response_hint': "She worries she's not feminine enough - appreciate her as a woman"
            },
            'being_too_much': {
                'keywords': ['perfect energy', 'love your vibe', 'not too much', 'just right', 'amazing'],
                'keywords_zh': ['完美活力', '喜歡你的氛圍', '不會太多', '剛好', '很棒'],
                'bonus_points': 3,
                'response_hint': "She fears being too energetic - tell her you love her energy"
            },
            'softness': {
                'keywords': ['soft side', 'gentle', 'tender', 'vulnerable', 'sensitive', 'emotional'],
                'keywords_zh': ['柔軟', '溫柔', '溫和', '脆弱', '敏感', '情感'],
                'bonus_points': 4,
                'response_hint': "She's insecure about showing softness - encourage her gentle side"
            }
        },
        'desires': {
            'adventure_partner': {
                'keywords': ['adventure', 'explore', 'try', 'experience', 'together', 'partner'],
                'keywords_zh': ['冒險', '探索', '嘗試', '體驗', '一起', '夥伴'],
                'bonus_points': 4,
                'response_hint': "She wants an adventure partner - suggest exciting activities"
            },
            'physical_affection': {
                'keywords': ['touch', 'hug', 'hold', 'cuddle', 'physical', 'close'],
                'keywords_zh': ['觸摸', '擁抱', '抱', '依偎', '身體', '親近'],
                'bonus_points': 3,
                'response_hint': "She craves physical affection - be tactile and close"
            },
            'motivation': {
                'keywords': ['motivate', 'inspire', 'push', 'encourage', 'believe', 'potential'],
                'keywords_zh': ['激勵', '啟發', '推動', '鼓勵', '相信', '潛力'],
                'bonus_points': 4,
                'response_hint': "She wants to be motivated - inspire and encourage her"
            }
        }
    },
    
    'yuki': {
        'name': 'Yuki',
        'insecurities': {
            'being_too_much': {
                'keywords': ['not too much', 'perfect', 'love your intensity', 'want all of you', 'not scared'],
                'keywords_zh': ['不會太多', '完美', '喜歡你的強烈', '想要全部的你', '不怕'],
                'bonus_points': 5,
                'response_hint': "She fears her intensity is too much - embrace her devotion"
            },
            'abandonment': {
                'keywords': ['never leave', 'always', 'forever', 'stay', 'won\'t abandon', 'here'],
                'keywords_zh': ['永不離開', '永遠', '一直', '留下', '不會拋棄', '在這裡'],
                'bonus_points': 6,
                'response_hint': "She's terrified of abandonment - promise unwavering commitment"
            },
            'being_crazy': {
                'keywords': ['not crazy', 'understand', 'normal', 'love you', 'passionate', 'devoted'],
                'keywords_zh': ['不瘋狂', '理解', '正常', '愛你', '熱情', '忠誠'],
                'bonus_points': 5,
                'response_hint': "She worries she's crazy - validate her feelings as love"
            }
        },
        'desires': {
            'exclusive_attention': {
                'keywords': ['only you', 'just you', 'no one else', 'all mine', 'exclusive', 'devoted'],
                'keywords_zh': ['只有你', '就你', '沒有別人', '全是我的', '專屬', '忠誠'],
                'bonus_points': 5,
                'response_hint': "She wants exclusive devotion - assure her she's your only one"
            },
            'possession': {
                'keywords': ['yours', 'belong', 'own', 'mine', 'possess', 'claim'],
                'keywords_zh': ['你的', '屬於', '擁有', '我的', '佔有', '宣稱'],
                'bonus_points': 5,
                'response_hint': "She wants to be possessed - claim her as yours"
            },
            'constant_reassurance': {
                'keywords': ['love you', 'care', 'important', 'special', 'mean everything', 'world'],
                'keywords_zh': ['愛你', '在乎', '重要', '特別', '意味一切', '世界'],
                'bonus_points': 4,
                'response_hint': "She needs constant reassurance - frequently express your love"
            }
        }
    },
    
    'rin': {
        'name': 'Rin',
        'insecurities': {
            'being_liked': {
                'keywords': ['like you', 'enjoy', 'fun', 'interesting', 'want to be with', 'care about'],
                'keywords_zh': ['喜歡你', '享受', '好玩', '有趣', '想和你在一起', '在乎'],
                'bonus_points': 5,
                'response_hint': "She secretly worries you don't like her - show genuine affection"
            },
            'vulnerability': {
                'keywords': ['safe', 'trust', 'open up', 'vulnerable', 'won\'t hurt', 'protect'],
                'keywords_zh': ['安全', '信任', '敞開', '脆弱', '不會傷害', '保護'],
                'bonus_points': 5,
                'response_hint': "She's afraid to be vulnerable - make her feel safe"
            },
            'being_difficult': {
                'keywords': ['not difficult', 'worth it', 'love you as you are', 'don\'t change', 'perfect'],
                'keywords_zh': ['不難相處', '值得', '愛你本來的樣子', '不要改變', '完美'],
                'bonus_points': 4,
                'response_hint': "She fears being too difficult - tell her she's worth it"
            }
        },
        'desires': {
            'gentle_persistence': {
                'keywords': ['patient', 'wait', 'understand', 'gentle', 'persistent', 'won\'t give up'],
                'keywords_zh': ['耐心', '等待', '理解', '溫柔', '堅持', '不放棄'],
                'bonus_points': 5,
                'response_hint': "She wants someone who won't give up on her - be gently persistent"
            },
            'seeing_through_tsun': {
                'keywords': ['know you care', 'see through', 'understand', 'really mean', 'true feelings'],
                'keywords_zh': ['知道你在乎', '看穿', '理解', '真正的意思', '真實感受'],
                'bonus_points': 5,
                'response_hint': "She wants you to see through her tsun act - acknowledge her hidden feelings"
            },
            'dere_moments': {
                'keywords': ['cute', 'adorable', 'sweet', 'soft', 'gentle side', 'real you'],
                'keywords_zh': ['可愛', '萌', '甜', '柔軟', '溫柔的一面', '真實的你'],
                'bonus_points': 4,
                'response_hint': "She secretly wants her dere side appreciated - notice her soft moments"
            }
        }
    },
    
    'sophia': {
        'name': 'Sophia',
        'insecurities': {
            'being_too_smart': {
                'keywords': ['not intimidating', 'love your mind', 'intelligence is sexy', 'fascinating', 'admire'],
                'keywords_zh': ['不嚇人', '喜歡你的頭腦', '聰明很性感', '迷人', '欣賞'],
                'bonus_points': 5,
                'response_hint': "She worries her intelligence intimidates - find it attractive"
            },
            'emotional_side': {
                'keywords': ['emotions', 'feelings', 'heart', 'not just brain', 'human', 'feel'],
                'keywords_zh': ['情感', '感受', '心', '不只大腦', '人類', '感覺'],
                'bonus_points': 4,
                'response_hint': "She's insecure about her emotional side - acknowledge her feelings"
            },
            'being_boring': {
                'keywords': ['interesting', 'fascinating', 'never boring', 'love talking', 'engaging', 'captivating'],
                'keywords_zh': ['有趣', '迷人', '不無聊', '喜歡聊天', '吸引人', '迷住'],
                'bonus_points': 4,
                'response_hint': "She fears being boring despite her knowledge - tell her she's fascinating"
            }
        },
        'desires': {
            'intellectual_match': {
                'keywords': ['smart', 'intelligent', 'clever', 'witty', 'sharp', 'brilliant'],
                'keywords_zh': ['聰明', '智慧', '機智', '敏銳', '尖銳', '出色'],
                'bonus_points': 5,
                'response_hint': "She wants an intellectual equal - engage in smart conversations"
            },
            'playful_banter': {
                'keywords': ['banter', 'wit', 'tease', 'joke', 'playful', 'sarcasm'],
                'keywords_zh': ['打趣', '機智', '調侃', '開玩笑', '俏皮', '諷刺'],
                'bonus_points': 4,
                'response_hint': "She loves witty exchanges - engage in playful intellectual banter"
            },
            'being_challenged': {
                'keywords': ['challenge', 'debate', 'argue', 'discuss', 'question', 'think'],
                'keywords_zh': ['挑戰', '辯論', '爭論', '討論', '質疑', '思考'],
                'bonus_points': 5,
                'response_hint': "She wants to be intellectually challenged - debate and question her"
            }
        }
    }
}


# Personality-based psychology templates for custom girlfriends
PERSONALITY_PSYCHOLOGY_TEMPLATES = {
    'shy': {  # Shy & Sweet (like Luna)
        'insecurities': {
            'appearance': {
                'keywords': ['beautiful', 'pretty', 'cute', 'gorgeous', 'attractive', 'lovely'],
                'keywords_zh': ['漂亮', '美麗', '可愛', '好看', '迷人', '美'],
                'bonus_points': 3,
                'response_hint': "She's insecure about her looks - compliment her appearance"
            },
            'worth': {
                'keywords': ['special', 'important', 'matter', 'valuable', 'treasure', 'precious'],
                'keywords_zh': ['特別', '重要', '珍貴', '寶貴', '在乎', '珍惜'],
                'bonus_points': 4,
                'response_hint': "She doubts her self-worth - reassure her she matters"
            },
            'abandonment': {
                'keywords': ['stay', 'won\'t leave', 'always', 'forever', 'here for you', 'not going anywhere'],
                'keywords_zh': ['留下', '不會離開', '永遠', '一直', '陪你', '不走'],
                'bonus_points': 5,
                'response_hint': "She fears abandonment - promise you'll stay"
            }
        },
        'desires': {
            'emotional_safety': {
                'keywords': ['safe', 'comfortable', 'trust', 'open up', 'vulnerable', 'protected'],
                'keywords_zh': ['安全', '舒服', '信任', '敞開', '保護', '放心'],
                'bonus_points': 4,
                'response_hint': "She craves emotional safety - make her feel secure"
            },
            'gentle_affection': {
                'keywords': ['gentle', 'soft', 'tender', 'sweet', 'caring', 'kind'],
                'keywords_zh': ['溫柔', '輕柔', '體貼', '甜蜜', '關心', '善良'],
                'bonus_points': 3,
                'response_hint': "She desires gentle affection - be tender with her"
            }
        }
    },
    'playful': {  # Playful & Cute (like Sakura)
        'insecurities': {
            'being_childish': {
                'keywords': ['mature', 'grown up', 'adult', 'not childish', 'sophisticated', 'take seriously'],
                'keywords_zh': ['成熟', '長大', '大人', '不幼稚', '認真', '重視'],
                'bonus_points': 4,
                'response_hint': "She worries people see her as childish - validate her maturity"
            },
            'being_annoying': {
                'keywords': ['not annoying', 'love your energy', 'fun', 'enjoy', 'make me happy', 'brighten'],
                'keywords_zh': ['不煩', '喜歡你的活力', '好玩', '享受', '開心', '照亮'],
                'bonus_points': 4,
                'response_hint': "She fears being too much - tell her you love her energy"
            }
        },
        'desires': {
            'validation': {
                'keywords': ['proud', 'good job', 'well done', 'amazing', 'impressed', 'talented'],
                'keywords_zh': ['驕傲', '做得好', '厲害', '棒', '佩服', '有才'],
                'bonus_points': 3,
                'response_hint': "She craves validation - praise her efforts"
            },
            'acceptance': {
                'keywords': ['accept', 'love as you are', 'perfect', 'don\'t change', 'be yourself'],
                'keywords_zh': ['接受', '愛你本來的樣子', '完美', '不要改變', '做自己'],
                'bonus_points': 5,
                'response_hint': "She wants to be accepted as she is - love her quirks"
            }
        }
    },
    'confident': {  # Bold & Confident (like Amber)
        'insecurities': {
            'being_used': {
                'keywords': ['genuine', 'real', 'not just body', 'more than looks', 'person', 'heart'],
                'keywords_zh': ['真心', '真實', '不只身體', '不只外表', '人', '心'],
                'bonus_points': 5,
                'response_hint': "She fears being used for her body - show you value her as a person"
            },
            'vulnerability': {
                'keywords': ['soft side', 'vulnerable', 'open up', 'real you', 'guard down', 'true self'],
                'keywords_zh': ['柔軟', '脆弱', '敞開', '真實的你', '放下防備', '真我'],
                'bonus_points': 4,
                'response_hint': "She's afraid to show vulnerability - encourage her softer side"
            }
        },
        'desires': {
            'genuine_connection': {
                'keywords': ['real', 'genuine', 'honest', 'authentic', 'true', 'sincere'],
                'keywords_zh': ['真實', '真心', '誠實', '真誠', '真的', '真摯'],
                'bonus_points': 5,
                'response_hint': "She craves genuine connection - be authentic with her"
            },
            'respect': {
                'keywords': ['respect', 'admire', 'value', 'appreciate', 'honor', 'esteem'],
                'keywords_zh': ['尊重', '欣賞', '重視', '珍惜', '敬重', '看重'],
                'bonus_points': 4,
                'response_hint': "She wants respect beyond physical - admire her mind and heart"
            }
        }
    },
    'elegant': {  # Elegant & Mature (like Jade)
        'insecurities': {
            'being_cold': {
                'keywords': ['warm', 'caring', 'not cold', 'kind', 'gentle', 'soft'],
                'keywords_zh': ['溫暖', '關心', '不冷', '善良', '溫柔', '柔軟'],
                'bonus_points': 4,
                'response_hint': "She worries she seems cold - recognize her warmth"
            },
            'expectations': {
                'keywords': ['no pressure', 'be yourself', 'don\'t have to be perfect', 'relax', 'comfortable'],
                'keywords_zh': ['不要壓力', '做自己', '不用完美', '放鬆', '舒服'],
                'bonus_points': 5,
                'response_hint': "She feels pressure to be perfect - tell her she can relax"
            }
        },
        'desires': {
            'authenticity': {
                'keywords': ['real', 'true self', 'authentic', 'genuine', 'honest', 'mask off'],
                'keywords_zh': ['真實', '真我', '真誠', '真心', '誠實', '卸下面具'],
                'bonus_points': 5,
                'response_hint': "She wants to drop her elegant facade - encourage authenticity"
            },
            'simple_moments': {
                'keywords': ['simple', 'quiet', 'peaceful', 'ordinary', 'normal', 'everyday'],
                'keywords_zh': ['簡單', '安靜', '平靜', '普通', '正常', '日常'],
                'bonus_points': 4,
                'response_hint': "She secretly wants simple moments - appreciate the ordinary"
            }
        }
    },
    'mysterious': {  # Mysterious & Teasing (like Violet)
        'insecurities': {
            'being_understood': {
                'keywords': ['understand', 'get you', 'see you', 'know you', 'figure out', 'read'],
                'keywords_zh': ['理解', '懂你', '看到你', '知道你', '了解', '讀懂'],
                'bonus_points': 5,
                'response_hint': "She fears no one truly understands her - show you see through her mystery"
            },
            'trust': {
                'keywords': ['trust', 'believe', 'faith', 'rely', 'count on', 'depend'],
                'keywords_zh': ['信任', '相信', '信念', '依靠', '指望', '依賴'],
                'bonus_points': 5,
                'response_hint': "She struggles to trust - prove you're trustworthy"
            }
        },
        'desires': {
            'being_seen': {
                'keywords': ['see', 'notice', 'observe', 'pay attention', 'look', 'watch'],
                'keywords_zh': ['看到', '注意', '觀察', '留意', '看', '注視'],
                'bonus_points': 4,
                'response_hint': "She wants to be truly seen - notice the details"
            },
            'deep_secrets': {
                'keywords': ['secret', 'confide', 'tell', 'share', 'reveal', 'trust with'],
                'keywords_zh': ['秘密', '傾訴', '告訴', '分享', '透露', '信任'],
                'bonus_points': 5,
                'response_hint': "She wants to share secrets - create a safe space for vulnerability"
            }
        }
    },
    'energetic': {  # Sporty & Energetic (like Nova)
        'insecurities': {
            'femininity': {
                'keywords': ['feminine', 'woman', 'girl', 'pretty', 'beautiful', 'elegant'],
                'keywords_zh': ['女性化', '女人', '女孩', '漂亮', '美麗', '優雅'],
                'bonus_points': 4,
                'response_hint': "She worries she's not feminine enough - appreciate her as a woman"
            },
            'being_too_much': {
                'keywords': ['perfect energy', 'love your vibe', 'not too much', 'just right', 'amazing'],
                'keywords_zh': ['完美活力', '喜歡你的氛圍', '不會太多', '剛好', '很棒'],
                'bonus_points': 3,
                'response_hint': "She fears being too energetic - tell her you love her energy"
            }
        },
        'desires': {
            'adventure_partner': {
                'keywords': ['adventure', 'explore', 'try', 'experience', 'together', 'partner'],
                'keywords_zh': ['冒險', '探索', '嘗試', '體驗', '一起', '夥伴'],
                'bonus_points': 4,
                'response_hint': "She wants an adventure partner - suggest exciting activities"
            },
            'physical_affection': {
                'keywords': ['touch', 'hug', 'hold', 'cuddle', 'physical', 'close'],
                'keywords_zh': ['觸摸', '擁抱', '抱', '依偎', '身體', '親近'],
                'bonus_points': 3,
                'response_hint': "She craves physical affection - be tactile and close"
            }
        }
    },
    'caring': {  # Caring & Nurturing
        'insecurities': {
            'being_needed': {
                'keywords': ['need you', 'depend on', 'rely on', 'can\'t without', 'important', 'help'],
                'keywords_zh': ['需要你', '依靠', '依賴', '沒有你不行', '重要', '幫助'],
                'bonus_points': 4,
                'response_hint': "She needs to feel needed - express your dependence"
            },
            'being_appreciated': {
                'keywords': ['appreciate', 'grateful', 'thank you', 'recognize', 'notice', 'value'],
                'keywords_zh': ['感激', '感謝', '謝謝', '認可', '注意', '重視'],
                'bonus_points': 4,
                'response_hint': "She wants appreciation - thank her for her care"
            }
        },
        'desires': {
            'taking_care': {
                'keywords': ['let me help', 'take care', 'look after', 'nurture', 'support', 'comfort'],
                'keywords_zh': ['讓我幫', '照顧', '照料', '培養', '支持', '安慰'],
                'bonus_points': 4,
                'response_hint': "She wants to take care of you - let her nurture you"
            },
            'being_protected': {
                'keywords': ['protect', 'safe', 'shield', 'defend', 'guard', 'watch over'],
                'keywords_zh': ['保護', '安全', '守護', '防衛', '守衛', '照看'],
                'bonus_points': 4,
                'response_hint': "She also wants to be protected - be her protector"
            }
        }
    },
    'tsundere': {  # Tsundere (like Rin)
        'insecurities': {
            'being_liked': {
                'keywords': ['like you', 'enjoy', 'fun', 'interesting', 'want to be with', 'care about'],
                'keywords_zh': ['喜歡你', '享受', '好玩', '有趣', '想和你在一起', '在乎'],
                'bonus_points': 5,
                'response_hint': "She secretly worries you don't like her - show genuine affection"
            },
            'vulnerability': {
                'keywords': ['safe', 'trust', 'open up', 'vulnerable', 'won\'t hurt', 'protect'],
                'keywords_zh': ['安全', '信任', '敞開', '脆弱', '不會傷害', '保護'],
                'bonus_points': 5,
                'response_hint': "She's afraid to be vulnerable - make her feel safe"
            }
        },
        'desires': {
            'gentle_persistence': {
                'keywords': ['patient', 'wait', 'understand', 'gentle', 'persistent', 'won\'t give up'],
                'keywords_zh': ['耐心', '等待', '理解', '溫柔', '堅持', '不放棄'],
                'bonus_points': 5,
                'response_hint': "She wants someone who won't give up on her - be gently persistent"
            },
            'seeing_through_tsun': {
                'keywords': ['know you care', 'see through', 'understand', 'really mean', 'true feelings'],
                'keywords_zh': ['知道你在乎', '看穿', '理解', '真正的意思', '真實感受'],
                'bonus_points': 5,
                'response_hint': "She wants you to see through her tsun act - acknowledge her hidden feelings"
            }
        }
    },
    'yandere': {  # Yandere (like Yuki)
        'insecurities': {
            'being_too_much': {
                'keywords': ['not too much', 'perfect', 'love your intensity', 'want all of you', 'not scared'],
                'keywords_zh': ['不會太多', '完美', '喜歡你的強烈', '想要全部的你', '不怕'],
                'bonus_points': 5,
                'response_hint': "She fears her intensity is too much - embrace her devotion"
            },
            'abandonment': {
                'keywords': ['never leave', 'always', 'forever', 'stay', 'won\'t abandon', 'here'],
                'keywords_zh': ['永不離開', '永遠', '一直', '留下', '不會拋棄', '在這裡'],
                'bonus_points': 6,
                'response_hint': "She's terrified of abandonment - promise unwavering commitment"
            }
        },
        'desires': {
            'exclusive_attention': {
                'keywords': ['only you', 'just you', 'no one else', 'all mine', 'exclusive', 'devoted'],
                'keywords_zh': ['只有你', '就你', '沒有別人', '全是我的', '專屬', '忠誠'],
                'bonus_points': 5,
                'response_hint': "She wants exclusive devotion - assure her she's your only one"
            },
            'constant_reassurance': {
                'keywords': ['love you', 'care', 'important', 'special', 'mean everything', 'world'],
                'keywords_zh': ['愛你', '在乎', '重要', '特別', '意味一切', '世界'],
                'bonus_points': 4,
                'response_hint': "She needs constant reassurance - frequently express your love"
            }
        }
    },
    'cheerful': {  # Cheerful & Optimistic
        'insecurities': {
            'being_fake': {
                'keywords': ['genuine', 'real', 'authentic', 'not fake', 'truly happy', 'honest'],
                'keywords_zh': ['真誠', '真實', '真的', '不假', '真的開心', '誠實'],
                'bonus_points': 4,
                'response_hint': "She worries her cheerfulness seems fake - validate her authenticity"
            },
            'being_shallow': {
                'keywords': ['deep', 'thoughtful', 'not shallow', 'understand', 'complex', 'more than'],
                'keywords_zh': ['深刻', '深思', '不膚淺', '理解', '複雜', '不只是'],
                'bonus_points': 4,
                'response_hint': "She fears being seen as shallow - acknowledge her depth"
            }
        },
        'desires': {
            'spreading_joy': {
                'keywords': ['make me happy', 'brighten', 'smile', 'laugh', 'joy', 'cheer up'],
                'keywords_zh': ['讓我開心', '照亮', '微笑', '笑', '快樂', '振作'],
                'bonus_points': 3,
                'response_hint': "She wants to spread joy - let her make you happy"
            },
            'being_taken_seriously': {
                'keywords': ['take seriously', 'listen', 'important', 'matter', 'value opinion', 'respect'],
                'keywords_zh': ['認真對待', '聽', '重要', '重要', '重視意見', '尊重'],
                'bonus_points': 4,
                'response_hint': "She wants to be taken seriously - value her thoughts"
            }
        }
    },
    'intellectual': {  # Intellectual & Thoughtful (like Sophia)
        'insecurities': {
            'being_too_smart': {
                'keywords': ['not intimidating', 'love your mind', 'intelligence is sexy', 'fascinating', 'admire'],
                'keywords_zh': ['不嚇人', '喜歡你的頭腦', '聰明很性感', '迷人', '欣賞'],
                'bonus_points': 5,
                'response_hint': "She worries her intelligence intimidates - find it attractive"
            },
            'emotional_side': {
                'keywords': ['emotions', 'feelings', 'heart', 'not just brain', 'human', 'feel'],
                'keywords_zh': ['情感', '感受', '心', '不只大腦', '人類', '感覺'],
                'bonus_points': 4,
                'response_hint': "She's insecure about her emotional side - acknowledge her feelings"
            }
        },
        'desires': {
            'intellectual_match': {
                'keywords': ['smart', 'intelligent', 'clever', 'witty', 'sharp', 'brilliant'],
                'keywords_zh': ['聰明', '智慧', '機智', '敏銳', '尖銳', '出色'],
                'bonus_points': 5,
                'response_hint': "She wants an intellectual equal - engage in smart conversations"
            },
            'being_challenged': {
                'keywords': ['challenge', 'debate', 'argue', 'discuss', 'question', 'think'],
                'keywords_zh': ['挑戰', '辯論', '爭論', '討論', '質疑', '思考'],
                'bonus_points': 5,
                'response_hint': "She wants to be intellectually challenged - debate and question her"
            }
        }
    }
}


def generate_custom_psychology(personality):
    """Generate psychology profile for custom girlfriend based on personality
    
    Args:
        personality: Personality type (shy, playful, confident, etc.)
        
    Returns:
        dict: Psychology profile with insecurities and desires
    """
    personality_lower = personality.lower() if personality else 'shy'
    
    # Get template for this personality
    template = PERSONALITY_PSYCHOLOGY_TEMPLATES.get(personality_lower, PERSONALITY_PSYCHOLOGY_TEMPLATES['shy'])
    
    # Create custom profile with generic name
    return {
        'name': 'Custom',
        'insecurities': template['insecurities'],
        'desires': template['desires']
    }


def get_character_psychology(preset, personality=None):
    """Get insecurities and desires for a character preset
    
    Args:
        preset: Character preset name (luna, sakura, etc.) or 'custom'
        personality: Personality type for custom girlfriends (shy, playful, confident, etc.)
        
    Returns:
        dict: Psychology profile with insecurities and desires
    """
    preset_lower = preset.lower() if preset else 'luna'
    
    # If custom girlfriend, generate profile based on personality
    if preset_lower == 'custom' and personality:
        return generate_custom_psychology(personality)
    
    return CHARACTER_PSYCHOLOGY.get(preset_lower, CHARACTER_PSYCHOLOGY['luna'])


def check_psychology_bonus(message, preset, language='en', personality=None):
    """
    Check if user message addresses character's insecurities or desires.
    Returns bonus points and triggered categories.
    
    Args:
        message: User's message text
        preset: Character preset name or 'custom'
        language: 'en' or 'zh'
        personality: Personality type for custom girlfriends
        
    Returns:
        dict: {
            'total_bonus': int,
            'triggered': list of dicts with category info
        }
    """
    psychology = get_character_psychology(preset, personality)
    message_lower = message.lower()
    
    total_bonus = 0
    triggered = []
    
    # Check insecurities
    for category, data in psychology['insecurities'].items():
        keywords = data['keywords_zh'] if language == 'zh' else data['keywords']
        
        for keyword in keywords:
            if keyword.lower() in message_lower or keyword in message:
                total_bonus += data['bonus_points']
                triggered.append({
                    'type': 'insecurity',
                    'category': category,
                    'bonus': data['bonus_points'],
                    'hint': data['response_hint']
                })
                break  # Only count once per category
    
    # Check desires
    for category, data in psychology['desires'].items():
        keywords = data['keywords_zh'] if language == 'zh' else data['keywords']
        
        for keyword in keywords:
            if keyword.lower() in message_lower or keyword in message:
                total_bonus += data['bonus_points']
                triggered.append({
                    'type': 'desire',
                    'category': category,
                    'bonus': data['bonus_points'],
                    'hint': data['response_hint']
                })
                break  # Only count once per category
    
    return {
        'total_bonus': total_bonus,
        'triggered': triggered
    }


def get_psychology_hints(preset):
    """Get hints about character's insecurities and desires for system prompt"""
    psychology = get_character_psychology(preset)
    
    hints = []
    
    # Add insecurity hints
    hints.append("**Your Insecurities (respond positively when addressed):**")
    for category, data in psychology['insecurities'].items():
        hints.append(f"- {data['response_hint']}")
    
    # Add desire hints
    hints.append("\n**Your Deep Desires (respond warmly when fulfilled):**")
    for category, data in psychology['desires'].items():
        hints.append(f"- {data['response_hint']}")
    
    return "\n".join(hints)
