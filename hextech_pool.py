from dataclasses import dataclass
from typing import Any

@dataclass
class Hextech:
    name: str           # 海克斯名稱
    tier: str           # 等級
    description: str    # 顯示的描述
    effect_type: str    # 效果類型 (例如 'add_score')
    effect_value: Any   # 變動的分數數值

# 這裡是你隨時可以擴充的「收容所」
HEXTECH_COLLECTION = {
#   "穩定發揮": Hextech(
#      tier="Silver",
#      description="展現基本功，該隊分數 +1",
#       effect_type="add_score",
#       effect_value=1
#   ),
    "強力扣殺": Hextech(
        name="強力扣殺",
        tier="Gold",
        description="球速驚人，該隊分數 +3",
        effect_type="add_score",
        effect_value=3
    ),
    "發球失誤": Hextech(
        name="發球失誤",
        tier="Silver",
        description="手感不佳，該隊分數 -1",
        effect_type="add_score",
        effect_value=-1
    ),
    "雙倍奉還": Hextech(
        name="雙倍奉還",
        tier="Prismatic",
        description="此後該隊每次得分變為 2 分",
        effect_type="modify_rate", 
        effect_value=2
    ),
    "手感發燙": Hextech(
        name="手感發燙",
        tier="Gold",
        description="此後該隊每次得分變為 3 分",
        effect_type="modify_rate",
        effect_value=3
    )
}
