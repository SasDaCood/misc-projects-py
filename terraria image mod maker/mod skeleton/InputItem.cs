using Terraria.ModLoader;
using static Terraria.ModLoader.ModContent;
using Terraria.ID;

namespace h
{
	public class InputItem:ModItem
	{
		public override void SetStaticDefaults() {
			DisplayName.SetDefault("h");
			Tooltip.SetDefault("aye");
		}

		public override void SetDefaults() {
			item.useStyle = 2;	// because why not
			item.useTurn = true;
			item.useAnimation = 15;
			item.useTime = 10;
			item.autoReuse = true;
			item.consumable = false;
			item.createTile = TileType<InputTile>();
			item.width = 24;	// resize input image to 12x12, and then upscale by 2x
			item.height = 24;
			item.rare = -12;
			item.value = 69;	// haha funny number
			item.maxStack = 69;
		}

		public override void AddRecipes() {
			ModRecipe recipe = new ModRecipe(mod);
			recipe.SetResult(this);
			recipe.AddRecipe();
		}
	}
}
