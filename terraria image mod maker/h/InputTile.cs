using Terraria;
using Terraria.ModLoader;
using Terraria.ObjectData;
using static Terraria.ModLoader.ModContent;

namespace h
{
	public class InputTile:ModTile
	{
		private const int WIDTH = 1496, HEIGHT = 1434;

		public override void SetDefaults() {
			Main.tileSolidTop[Type] = true;
			Main.tileFrameImportant[Type] = true;

			TileObjectData.newTile.Width = 1;
			TileObjectData.newTile.Height = 1;
			TileObjectData.newTile.CoordinateWidth = WIDTH;
			TileObjectData.newTile.CoordinateHeights = new int[] {HEIGHT};
			TileObjectData.newTile.DrawYOffset = 16-HEIGHT;
			TileObjectData.newTile.UsesCustomCanPlace = true;
			TileObjectData.addTile(Type);
			drop = ItemType<InputItem>();
		}
	}
}