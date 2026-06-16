import os


def main():
    targets = [
        "netherite_sword",
        "netherite_pickaxe",
        "netherite_shovel",
        "netherite_axe",
        "netherite_hoe",
        "netherite_spear",
        "netherite_helmet",
        "netherite_chestplate",
        "netherite_leggings",
        "netherite_boots",
        "shield",
        "bow",
        "crossbow",
        "mace",
        "elytra",
        "trident",
    ]
    print("本脚本适用于 Minecraft Java 26.1.2")
    name = input(
        "输入目标物品命名空间ID(留空输出所有常用装备并生成数据包)\n输入："
    ).strip()
    if not name:
        print("将生成所有常用装备命令并生成一键执行数据包")
    lvl = input("输入附魔等级（最高255）：").strip()
    cmd_list = []
    try:
        lvl = max(1, min(int(lvl), 255))
    except:
        lvl = 255
    if name:
        make_commands(name, lvl)
    else:
        print(f"将输出共 {len(targets)} 个魔咒命令")
        for n in targets:
            res = make_commands(n, lvl)
            cmd_list.append(res)
        build_datapack(cmd_list, lvl)


def make_commands(name, lvl):
    # 灵魂疾行、迅捷潜行、冰霜行者、快速装填、时运、抢夺、突进、风爆,本脚本限制最高5级
    # 忠诚与激流不能同时存在,激流禁用了三叉戟的投掷
    # 绑定诅咒、消失诅咒不使用
    # 限制最高等级
    limit_5 = {
        "fortune",
        "frost_walker",
        "quick_charge",
        "soul_speed",
        "swift_sneak",
        "looting",
        "lunge",
        "wind_burst",
    }
    enchantments = [
        "aqua_affinity",
        "bane_of_arthropods",
        "blast_protection",
        "breach",
        "channeling",
        "density",
        "depth_strider",
        "efficiency",
        "feather_falling",
        "fire_aspect",
        "fire_protection",
        "flame",
        "impaling",
        "infinity",
        "knockback",
        "loyalty",
        "luck_of_the_sea",
        "lure",
        "mending",
        "multishot",
        "piercing",
        "power",
        "projectile_protection",
        "protection",
        "punch",
        "respiration",
        # "riptide",  # 激流
        "sharpness",
        "silk_touch",
        "smite",
        "sweeping_edge",
        "thorns",
        "unbreaking",
    ]
    len_enchantments = len(enchantments)
    len_limit_5 = len(limit_5)
    enchantments += limit_5
    ench_list = []
    for ench in enchantments:
        value = 5 if ench in limit_5 else lvl
        ench_list.append(f'"minecraft:{ench}":{value}')
    ench_str = ",".join(ench_list)
    command = (
        f"give @p {name}["
        f"minecraft:enchantments={{{ench_str}}},"
        f"minecraft:unbreakable={{}},"
        f'minecraft:lore=["Hello"],'
        f"minecraft:tooltip_display={{hide_tooltip:true}},"
        f'minecraft:custom_name={{"text":"全附魔{lvl}级_{name}","color":"gold"}}'
        f"] 1"
    )
    print(f"[魔咒总数:{len_enchantments+len_limit_5}]{name}的生成结果：")
    print(command)
    print()
    return command


def build_datapack(cmd_list, lvl, pack_name="mc_func", namespace="mc_func"):
    """
    cmd_list: list[str]  -> 每一条 Minecraft 命令（如 give / tp / say 等）
    pack_name: 数据包文件夹名称
    namespace: /function 的命名空间
    """
    base = os.path.join(os.getcwd(), pack_name)
    data_path = os.path.join(base, "data", namespace, "function", ".ench")
    item_data_path = os.path.join(base, "data", namespace, "function", ".item")
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(item_data_path, exist_ok=True)
    pack_mcmeta = """{
  "pack": {
    "description": "MC_Function",
    "min_format": [
      101,
      1
    ],
    "max_format": 101
  }
}
    """
    with open(os.path.join(base, "pack.mcmeta"), "w", encoding="utf-8") as f:
        f.write(pack_mcmeta)
    func_path = os.path.join(data_path, f"give_{lvl}.mcfunction")
    with open(func_path, "w", encoding="utf-8") as f:
        for cmd in cmd_list:
            cmd = cmd.strip()
            if cmd:
                f.write(cmd + "\n")
    item_replacd_path = os.path.join(item_data_path, f"item_replace.mcfunction")
    item_replacd_cmd = [
        "item replace entity @a container.9 with minecraft:arrow 64",
        "item replace entity @a container.10 with minecraft:firework_rocket 64",
        "item replace entity @a container.11 with minecraft:ender_pearl 16",
        "kill @e[type = item, nbt = {Item: {id: \"minecraft:ender_pearl\"}}]",
        "kill @e[type = item, nbt = {Item: {id: \"minecraft:arrow\"}}]",
        "kill @e[type = item, nbt = {Item: {id: \"minecraft:firework_rocket\"}}]"
    ]
    with open(item_replacd_path, "w", encoding="utf-8") as f:
        for cmd in item_replacd_cmd:
            cmd = cmd.strip()
            if cmd:
                f.write(cmd + "\n")
    print("\n数据包已生成！")
    print("路径：", base)
    print("将数据包文件夹整个放入存档datapacks文件夹,然后/reload")
    print(f"执行命令： /function {namespace}:.ench/give_{lvl}")


if __name__ == "__main__":
    main()
