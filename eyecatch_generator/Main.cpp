#include <Siv3D.hpp>
#include <array>
#include <filesystem>

namespace
{
	constexpr Size WindowSize{ 1120, 720 };
	constexpr RectF Editor{ 24, 84, 670, 574 };
	constexpr RectF Settings{ 710, 84, 386, 574 };
	constexpr RectF SourceArea{ 40, 136, 638, 476 };
	constexpr RectF PreviewArea{ 728, 132, 350, 216 };
	constexpr ColorF Background{ 0.067, 0.082, 0.102 };
	constexpr ColorF Panel{ 0.102, 0.126, 0.153 };
	constexpr ColorF Canvas{ 0.051, 0.064, 0.081 };
	constexpr ColorF Border{ 0.223, 0.260, 0.308 };
	constexpr ColorF Text{ 0.93, 0.96, 0.98 };
	constexpr ColorF Muted{ 0.69, 0.75, 0.81 };
	constexpr ColorF Accent{ 0.39, 0.90, 0.77 };
	constexpr ColorF ErrorText{ 1.0, 0.65, 0.59 };

	constexpr std::array EyecatchSizes{ Size{ 1200, 720 }, Size{ 1280, 720 }, Size{ 1280, 768 } };
	constexpr std::array TileSizes{ Size{ 512, 512 }, Size{ 256, 256 } };
	constexpr std::array RibbonLabels{ U"なし", U"金", U"銀", U"銅", U"青" };
	constexpr std::array RibbonPaths{ U"gold.png", U"silver.png", U"bronze.png", U"blue.png" };
	// works.svg places a 20-unit wide ribbon on a 100-unit tile.
	constexpr double RibbonWidthRatio = 0.2;

	RectF Fit(const Size imageSize, const RectF area)
	{
		const double scale = Min(area.w / imageSize.x, area.h / imageSize.y);
		const Vec2 size = Vec2{ imageSize } * scale;
		return{ area.center() - size * 0.5, size };
	}

	String Dimensions(const Size size)
	{
		return Format(size.x, U"×", size.y);
	}

	bool Button(const RectF area, const Font& font, const StringView label,
		const bool selected = false, const bool enabled = true, const bool primary = false)
	{
		const bool hover = enabled && area.mouseOver();
		if (hover)
		{
			Cursor::RequestStyle(CursorStyle::Hand);
		}
		const ColorF fill = (enabled && primary) ? Accent
			: (hover || selected) ? ColorF{ 0.16, 0.24, 0.28 } : Panel;
		area.rounded(7).draw(fill).drawFrame(1, (selected || hover) ? Accent : Border);
		const ColorF labelColor = !enabled ? Muted : primary ? Canvas : selected ? Accent : Text;
		font(label).drawAt(area.center(), labelColor);
		return hover && MouseL.down();
	}

	class CropSelection
	{
	public:
		RectF area{};

		void reset(const Size imageSize, const double aspect)
		{
			bounds = imageSize;
			ratio = aspect;
			drag = Drag::None;
			const double width = maxWidth();
			area = { Vec2{ (bounds.x - width) * 0.5, (bounds.y - width / ratio) * 0.5 }, width, width / ratio };
		}

		void setAspect(const double aspect)
		{
			if (ratio == aspect) return;
			ratio = aspect;
			drag = Drag::None;
			const Vec2 center = area.center();
			const double width = Clamp(Sqrt(area.w * area.h * ratio), minWidth(), maxWidth());
			place(center - Vec2{ width, width / ratio } * 0.5, width);
		}

		RectF onScreen(const RectF image) const
		{
			const double scale = image.w / bounds.x;
			return{ image.pos + area.pos * scale, area.size * scale };
		}

		void update(const RectF image)
		{
			const Vec2 cursor = Cursor::PosF();
			const Vec2 point = (cursor - image.pos) * (bounds.x / image.w);
			const RectF screenCrop = onScreen(image);
			const std::array corners{ screenCrop.tl(), screenCrop.tr(), screenCrop.br(), screenCrop.bl() };
			int32 corner = -1;
			double closest = 10;
			for (int32 i = 0; i < static_cast<int32>(corners.size()); ++i)
			{
				const double distance = cursor.distanceFrom(corners[i]);
				if (distance < closest)
				{
					closest = distance;
					corner = i;
				}
			}

			if (MouseL.down())
			{
				if (corner >= 0 && SourceArea.mouseOver())
				{
					const Vec2 opposite = corners[(corner + 2) % corners.size()];
					anchor = (opposite - image.pos) * (bounds.x / image.w);
					const Vec2 direction = corners[corner] - opposite;
					sign = { direction.x < 0 ? -1.0 : 1.0, direction.y < 0 ? -1.0 : 1.0 };
					handleOffset = (corners[corner] - cursor) * (bounds.x / image.w);
					drag = Drag::Resize;
				}
				else if (screenCrop.mouseOver())
				{
					anchor = point - area.pos;
					drag = Drag::Move;
				}
				else if (image.mouseOver())
				{
					anchor = point;
					drag = Drag::New;
				}
			}

			if (!MouseL.pressed() && !MouseL.up()) drag = Drag::None;
			if (drag == Drag::Move) place(point - anchor, area.w);
			if (drag == Drag::Resize) resizeTo(point + handleOffset, sign);
			if (drag == Drag::New)
			{
				const Vec2 delta = point - anchor;
				if (delta.length() * image.w / bounds.x >= 4)
				{
					resizeTo(point, { delta.x < 0 ? -1.0 : 1.0, delta.y < 0 ? -1.0 : 1.0 });
				}
			}
			if (MouseL.up()) drag = Drag::None;

			if (drag == Drag::None && image.mouseOver() && Mouse::Wheel() != 0)
			{
				const Vec2 fixed = screenCrop.mouseOver() ? point : area.center();
				const double width = Clamp(area.w * std::pow(1.14, Mouse::Wheel()), minWidth(), maxWidth());
				place(fixed - (fixed - area.pos) * (width / area.w), width);
			}

			if (drag == Drag::Move) Cursor::RequestStyle(CursorStyle::ResizeAll);
			else if (drag == Drag::Resize) Cursor::RequestStyle(sign.x == sign.y ? CursorStyle::ResizeNWSE : CursorStyle::ResizeNESW);
			else if (drag == Drag::New) Cursor::RequestStyle(CursorStyle::Cross);
			else if (corner >= 0 && SourceArea.mouseOver()) Cursor::RequestStyle(corner % 2 == 0 ? CursorStyle::ResizeNWSE : CursorStyle::ResizeNESW);
			else if (screenCrop.mouseOver()) Cursor::RequestStyle(CursorStyle::ResizeAll);
			else if (image.mouseOver()) Cursor::RequestStyle(CursorStyle::Cross);
		}

	private:
		enum class Drag { None, Move, Resize, New };
		Vec2 bounds{};
		double ratio = 1;
		Drag drag = Drag::None;
		Vec2 anchor;
		Vec2 sign;
		Vec2 handleOffset;

		double maxWidth() const { return Min(bounds.x, bounds.y * ratio); }
		double minWidth() const { return Min(12.0, maxWidth()); }

		void place(const Vec2 origin, const double width)
		{
			const Vec2 size{ width, width / ratio };
			area = { Clamp(origin.x, 0.0, Max(0.0, bounds.x - size.x)),
				Clamp(origin.y, 0.0, Max(0.0, bounds.y - size.y)), size.x, size.y };
		}

		void resizeTo(const Vec2 point, const Vec2 direction)
		{
			const Vec2 delta = point - anchor;
			const double spaceX = direction.x > 0 ? bounds.x - anchor.x : anchor.x;
			const double spaceY = direction.y > 0 ? bounds.y - anchor.y : anchor.y;
			const double widthLimit = Min(spaceX, spaceY * ratio);
			if (widthLimit < minWidth()) return;

			const double heightPerWidth = 1.0 / ratio;
			const double projectedWidth = (delta.x * direction.x + delta.y * direction.y * heightPerWidth)
				/ (1.0 + heightPerWidth * heightPerWidth);
			const double width = Clamp(projectedWidth, minWidth(), widthLimit);
			place({ anchor.x - (direction.x < 0 ? width : 0.0),
				anchor.y - (direction.y < 0 ? width / ratio : 0.0) }, width);
		}
	};

	Texture LoadSource(const FilePath& path)
	{
		Image image{ path };
		if (!image) return {};
		const String extension = FileSystem::Extension(path).lowercased();
		if (extension == U"jpg" || extension == U"jpeg")
		{
			if (const auto exif = Exif::Read(path))
			{
				switch (exif->orientation)
				{
				case 2: image.mirror(); break;
				case 3: image.rotate180(); break;
				case 4: image.flip(); break;
				case 5: image.rotate90().mirror(); break;
				case 6: image.rotate90(); break;
				case 7: image.rotate90().flip(); break;
				case 8: image.rotate270(); break;
				}
			}
		}
		for (Color& pixel : image)
		{
			if (pixel.a == 255) continue;
			const auto overWhite = [alpha = pixel.a](const uint8 value)
			{
				return static_cast<uint8>(255 - ((255 - value) * alpha + 127) / 255);
			};
			pixel.set(overWhite(pixel.r), overWhite(pixel.g), overWhite(pixel.b), 255);
		}
		return Texture{ image, TextureDesc::Mipped };
	}

	void DrawCrop(const Texture& source, const RectF image, const RectF crop)
	{
		source.resized(image.size).draw(image.pos);
		const ColorF veil{ 0.025, 0.035, 0.05, 0.64 };
		RectF{ image.x, image.y, image.w, Max(0.0, crop.y - image.y) }.draw(veil);
		RectF{ image.x, crop.bottomY(), image.w, Max(0.0, image.bottomY() - crop.bottomY()) }.draw(veil);
		RectF{ image.x, crop.y, Max(0.0, crop.x - image.x), crop.h }.draw(veil);
		RectF{ crop.rightX(), crop.y, Max(0.0, image.rightX() - crop.rightX()), crop.h }.draw(veil);

		for (int32 i = 1; i <= 2; ++i)
		{
			const double x = crop.x + i * crop.w / 3;
			const double y = crop.y + i * crop.h / 3;
			Line{ x, crop.y, x, crop.bottomY() }.draw(1, ColorF{ 1.0, 0.44 });
			Line{ crop.x, y, crop.rightX(), y }.draw(1, ColorF{ 1.0, 0.44 });
		}
		crop.drawFrame(2, 0, Accent);
		for (const Vec2 corner : { crop.tl(), crop.tr(), crop.br(), crop.bl() })
		{
			Circle{ corner, 4.5 }.draw(Accent).drawFrame(1, Canvas);
		}
	}

	RenderTexture Compose(const Texture& source, const RectF crop, const Size size,
		const Texture& ribbon, RenderTexture target)
	{
		if (target.size() != size) target = RenderTexture{ size };
		if (!target) return {};
		const double w = source.width();
		const double h = source.height();
		const ScopedRenderTarget2D renderTarget{ target };
		const ScopedRenderStates2D sampler{ SamplerState::ClampAniso };
		source.uv(crop.x / w, crop.y / h, crop.w / w, crop.h / h).resized(size).draw();
		if (ribbon)
		{
			const double width = Min(size.x, size.y) * RibbonWidthRatio;
			ribbon.resized(width, width * ribbon.height() / ribbon.width()).draw();
		}
		return target;
	}

	bool SaveJpeg(const RenderTexture& output, const FilePath& path)
	{
		Image image;
		Graphics2D::Flush();
		output.readAsImage(image);
		if (image.size() != output.size()) return false;

		// Encode alongside the destination so a failed write cannot truncate an existing JPEG.
		const FilePath temp = FileSystem::UniqueFilePath(FileSystem::ParentPath(path));
		if (temp.isEmpty()) return false;
		std::error_code error;
		const bool encoded = JPEGEncoder{}.save(image, temp, 93);
		if (encoded)
		{
			std::filesystem::rename(Unicode::ToWstring(temp), Unicode::ToWstring(path), error);
			if (!error) return true;
		}
		FileSystem::Remove(temp);
		return false;
	}
}

void Main()
{
	Window::SetTitle(U"アイキャッチ画像作成");
	Window::Resize(WindowSize);
	Window::SetStyle(WindowStyle::Sizable);
	Window::SetMinimumFrameBufferSize({ 780, 500 });
	// Keep the layout and pointer coordinates in one coordinate system as the window scales.
	Scene::SetResizeMode(ResizeMode::Keep);
	Scene::Resize(WindowSize);
	Scene::SetBackground(Background);
	System::SetTerminationTriggers(UserAction::CloseButtonClicked);
	DragDrop::AcceptFilePaths(true);

	const Font title{ 28, Typeface::Bold };
	const Font section{ 18, Typeface::Bold };
	const Font body{ 15, Typeface::Regular };
	const Font small{ 13, Typeface::Regular };
	const Array<FileFilter> openFilters{
		{ U"画像ファイル", { U"jpg", U"jpeg", U"png", U"webp", U"bmp" } }, FileFilter::AllFiles()
	};
	const Array<FileFilter> saveFilters{ FileFilter::JPEG() };

	std::array<Texture, RibbonLabels.size()> ribbons;
	for (size_t i = 0; i < RibbonPaths.size(); ++i)
	{
		ribbons[i + 1] = Texture{ Resource(U"ribbons/" + String{ RibbonPaths[i] }), TextureDesc::Mipped };
	}

	Texture source;
	RenderTexture output;
	CropSelection crop;
	FilePath sourcePath;
	FilePath lastSaveDirectory;
	String status;
	bool errorStatus = false;
	bool tile = false;
	size_t eyecatchSize = 0;
	size_t tileSize = 0;
	size_t ribbon = 0;
	const auto outputSize = [&] { return tile ? TileSizes[tileSize] : EyecatchSizes[eyecatchSize]; };
	const auto aspect = [&] { return static_cast<double>(outputSize().x) / outputSize().y; };
	const auto report = [&](String message, const bool error = false)
	{
		status = std::move(message);
		errorStatus = error;
	};

	while (System::Update())
	{
		RectF{ 0, 0, WindowSize.x, 69 }.draw(Panel);
		Line{ 0, 69, WindowSize.x, 69 }.draw(1, Border);
		title(U"アイキャッチ画像作成").draw(24, 14, Text);
		const bool openRequested = Button({ 939, 16, 157, 38 }, body, U"画像を開く", false, true, true)
			|| (KeyControl + KeyO).down();
		const bool saveShortcut = (KeyControl + KeyS).down();
		FilePath newPath;
		const auto dropped = DragDrop::GetDroppedFilePaths();
		if (!dropped.empty()) newPath = dropped.front().path;
		if (openRequested)
		{
			newPath = Dialog::OpenFile(openFilters, sourcePath.isEmpty() ? U"" : FileSystem::ParentPath(sourcePath),
				U"切り取る画像を選択").value_or(U"");
		}
		bool loaded = false;
		if (!newPath.isEmpty())
		{
			if (Texture candidate = LoadSource(newPath))
			{
				source = std::move(candidate);
				sourcePath = std::move(newPath);
				crop.reset(source.size(), aspect());
				loaded = true;
				report(U"");
			}
			else
			{
				report(U"画像を読み込めませんでした", true);
			}
		}

		Editor.rounded(12).draw(Panel).drawFrame(1, Border);
		Settings.rounded(12).draw(Panel).drawFrame(1, Border);
		section(U"元画像").draw(40, 99, Text);
		section(U"出力プレビュー").draw(728, 99, Text);
		const Size previousSize = outputSize();
		const size_t previousRibbon = ribbon;
		const RectF previousCrop = crop.area;
		const bool reset = Button({ 555, 96, 123, 30 }, small, U"枠をリセット", false, static_cast<bool>(source));
		if (Button({ 728, 365, 170, 35 }, body, U"アイキャッチ", !tile)) tile = false;
		if (Button({ 908, 365, 170, 35 }, body, U"正方形タイル", tile)) tile = true;

		small(U"出力サイズ（px）").draw(728, 414, Muted);
		const auto drawSizes = [&](const auto& sizes, size_t& active)
		{
			const double width = (350.0 - 8.0 * (sizes.size() - 1)) / sizes.size();
			for (size_t i = 0; i < sizes.size(); ++i)
			{
				if (Button({ 728 + i * (width + 8), 439, width, 34 }, body, Dimensions(sizes[i]), active == i)) active = i;
			}
		};
		if (tile) drawSizes(TileSizes, tileSize);
		else drawSizes(EyecatchSizes, eyecatchSize);

		small(U"受賞リボン").draw(728, 491, Muted);
		for (size_t i = 0; i < RibbonLabels.size(); ++i)
		{
			const RectF option{ 728.0 + i * 71, 516, 66, 37 };
			const bool available = (i == 0 || static_cast<bool>(ribbons[i]));
			if (Button(option, body, i == 0 ? U"なし" : U"", i == ribbon, available)) ribbon = i;
			if (i != 0)
			{
				if (available) ribbons[i].resized(15).draw(option.x + 11, option.y + 8);
				body(RibbonLabels[i]).drawAt(option.x + 44, option.centerY(), available ? Text : Muted);
				if (!available && option.mouseOver()) report(U"受賞リボンの素材を読み込めませんでした", true);
			}
		}
		const bool saveClicked = Button({ 728, 597, 350, 44 }, section, U"名前をつけてJPEG保存",
			false, static_cast<bool>(source), true);

		SourceArea.rounded(7).draw(Canvas);
		PreviewArea.rounded(7).draw(Canvas);
		if (source)
		{
			if (reset) crop.reset(source.size(), aspect());
			else if (outputSize() != previousSize) crop.setAspect(aspect());
			const RectF image = Fit(source.size(), SourceArea.stretched(-8));
			crop.update(image);
			DrawCrop(source, image, crop.onScreen(image));
			const String sourceLabel = FileSystem::FileName(sourcePath) + U"   " + Dimensions(source.size()) + U" px";
			small(sourceLabel).draw(RectF{ 40, 621, 638, 26 }, Muted);

			const bool changed = (crop.area != previousCrop || outputSize() != previousSize || ribbon != previousRibbon);
			if (changed && !errorStatus) report(U"");
			if (loaded || !output || changed)
			{
				output = Compose(source, crop.area, outputSize(), ribbons[ribbon], std::move(output));
			}
			if (output)
			{
				const RectF preview = Fit(output.size(), PreviewArea.stretched(-4));
				output.resized(preview.size).draw(preview.pos);
			}
		}
		else
		{
			section(U"画像をここにドロップ").drawAt(SourceArea.center(), Text);
			body(U"画像を開くとプレビューが表示されます").drawAt(PreviewArea.center(), Muted);
		}
		if (DragDrop::DragOver()) SourceArea.rounded(7).drawFrame(2, Accent);

		if ((saveClicked || saveShortcut) && output)
		{
			const String sourceName = FileSystem::BaseName(sourcePath);
			const String name = tile ? (sourceName == U"eyecatch" ? U"tile" : sourceName + U"-tile") : U"eyecatch";
			const FilePath directory = lastSaveDirectory.isEmpty() ? FileSystem::ParentPath(sourcePath) : lastSaveDirectory;
			if (const auto path = Dialog::SaveFile(saveFilters, directory, U"JPEGのファイル名と保存先を指定", name + U".jpg"))
			{
				const String extension = FileSystem::Extension(*path).lowercased();
				if (extension != U"jpg" && extension != U"jpeg")
				{
					report(U"ファイル名の拡張子を .jpg または .jpeg にしてください", true);
				}
				else if (SaveJpeg(output, *path))
				{
					lastSaveDirectory = FileSystem::ParentPath(*path);
					report(U"保存しました　" + FileSystem::FileName(*path));
				}
				else
				{
					report(U"JPEGの保存に失敗しました", true);
				}
			}
		}

		const StringView cropHint = U"枠内ドラッグで移動　角またはホイールでサイズ調整　枠外からドラッグで範囲を選択";
		small(source ? cropHint : U"対応形式　JPEG・PNG・WebP・BMP").draw(25, 670, Muted);
		if (!status.isEmpty()) small(status).draw(RectF{ 25, 691, 1068, 25 }, errorStatus ? ErrorText : Accent);
	}
}
