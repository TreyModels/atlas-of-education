# Atlas mô hình phát triển và giáo dục

8 tháng 11 năm 2026 · James W. Menefee III

## Cách dùng danh mục

Mỗi mục đưa ra một nhận định về cách một hệ thống vận hành để có thể triển khai thành mô hình chạy được trong Atlas. Các mô hình giải thích cùng một kết quả được chấm trên cùng dữ liệu.

Mỗi mục ghi:

- **Nhận định**: kết quả cần giải thích trong một câu.
- **Cơ chế**: quy tắc nhân quả viết bằng ngôn ngữ dễ hiểu.
- **Phương trình hoặc quy tắc**: vị trí trong bài báo, phụ lục hoặc mã.
- **Mã và dữ liệu**: tài liệu công khai và giấy phép.
- **Kiểm định độ khớp**: mẫu hình quan sát cần tái tạo.
- **Mô hình đối chiếu**: các cách giải thích khác cho cùng kết quả.

| Trạng thái | Ý nghĩa |
| --- | --- |
| Đang chạy | Đã có mô hình trong Atlas |
| Chuyển mã | Có mã hoặc dữ liệu công khai để điều chỉnh |
| Xây dựng | Phương trình đã công bố, có thể triển khai từ bài báo |
| Lập luận | Có dữ liệu nhưng chưa có mô hình hình thức |
| Mô hình nặng | Cần Dynare, MATLAB hoặc dữ liệu vi mô lớn |

## Tăng trưởng Trung Quốc và các cơ chế cạnh tranh

Ba mô hình giải thích đầu tư tăng, tỷ phần thu nhập lao động giảm và thặng dư đối ngoại tăng bằng những nguyên nhân khác nhau. Chấm trên cùng bộ dữ liệu giúp thấy rõ khác biệt.

| Mô hình | Cơ chế | Trạng thái | Kiểm định |
| --- | --- | --- | --- |
| [Song, Storesletten và Zilibotti, *Growing Like China* (2011)](https://econpapers.repec.org/RePEc:aea:aecrev:v:101:y:2011:i:1:p:196-233) | Ma sát tín dụng. Doanh nghiệp tư nhân năng suất cao tự tài trợ, doanh nghiệp năng suất thấp sống nhờ dễ tiếp cận tín dụng | Chuyển mã. Dữ liệu AER và [mã tác giả](https://campuspress.yale.edu/zilibotti/published-research) | Lợi tức vốn bền, sản xuất dịch chuyển sang tư nhân, thặng dư từ 1992 |
| [Chang, Chen, Waggoner và Zha, xu hướng và chu kỳ vĩ mô Trung Quốc (2015)](https://www.nber.org/papers/w21244) | Tín dụng ưu đãi cho công nghiệp nặng | Mô hình DSGE hai ngành, có thể rút gọn còn quy tắc phân bổ tín dụng | Đầu tư và tiêu dùng ít đồng biến, tỷ lệ đầu tư tăng, tỷ phần lao động giảm |
| [Bai, Hsieh và Song, tác động dài hạn của mở rộng tài khóa (2016)](https://www.nber.org/papers/w22801) | Kích thích 2009–10 qua công cụ tài chính ngoài bảng cân đối của địa phương, ưu tiên doanh nghiệp có quan hệ | Xây dựng quy tắc vay thế chấp đất từ lập luận | Đầu tư tăng lâu dài sau 2010, chi ngoài bảng cân đối khoảng 5% GDP mỗi năm sau kích thích |

**Dữ liệu chung**: tỷ lệ đầu tư, tỷ phần lao động, tài khoản vãng lai và tỷ phần sản lượng tư nhân so với nhà nước, 1992–2024. Chuỗi vĩ mô năm và quý của Chang và cộng sự có thể làm bộ dữ liệu chung.

**Câu hỏi mở**: cải cách giá hai đường ray của Isabella Weber là một cách giải thích cho giai đoạn đầu thập niên 1980, chưa được mô hình hóa hình thức.

## Tín dụng và bất động sản Trung Quốc

Lập luận về tín dụng có bằng chứng nhưng chưa có mô hình công khai. Hai nghiên cứu nhà ở khác nhau về vai trò khởi phát hay khuếch đại khủng hoảng của bất động sản.

| Nghiên cứu | Lập luận | Trạng thái |
| --- | --- | --- |
| [Logan Wright, *Broken China* (2026)](https://fsi.stanford.edu/node/39615) | Tăng trưởng chậm lại bắt nguồn từ hệ thống tài chính và việc kết thúc mở rộng tín dụng chưa từng có. Xem [*Credit and Credibility* (2018)](https://www.csis.org/analysis/credit-and-credibility-risks-chinas-economic-resilience) | Lập luận |
| [Rogoff và Yang, *Peak China Housing* (2020)](https://www.nber.org/papers/w27697) | Nhà ở và ngành liên quan chiếm khoảng 29% GDP. Suy giảm nhà ở làm sản lượng giảm lũy kế 5–10% | Xây dựng hệ số đầu vào–đầu ra dùng được trên trình duyệt |
| [Fang, Gu, Xiong và Zhou, bùng nổ nhà ở Trung Quốc (2015)](https://www.nber.org/papers/w21112) | Giá tăng cùng thu nhập. Trả trước trên 35% khiến nhà ở khuếch đại cú sốc | Xây dựng quy tắc giá trên thu nhập và đòn bẩy theo nhóm người mua |
| [Tianlei Huang, *Detox* (sắp xuất bản)](https://www.pulse.bot/real-estate/news/understanding-chinas-economy-and-the-housing-bust-with-tianlei-huang-aab32144-79af-4919-be93-176d6e7de292/) | Suy giảm buộc chính quyền địa phương xử lý vấn đề tài khóa | Lập luận |

**Mô hình đề xuất**: tín dụng và nhà ở nhất quán tồn lượng–luồng, gồm hộ gia đình, chủ đầu tư, công cụ tài chính địa phương, ngân hàng và trung ương. Mỗi khoản vay là tài sản của một bên nên bảng cân đối phải khớp từng kỳ. Điều chỉnh mức phụ thuộc bán đất, tài trợ bán trước, quy tắc trả trước, mục tiêu tín dụng và gia hạn của ngân hàng. Kiểm định đòn bẩy hộ, thời điểm vỡ nợ sau giới hạn vay năm 2020 và tỷ trọng thu đất trong ngân sách địa phương.

Có thể dùng khung Godley–Lavoie với gói R `sfcr` hoặc Minsky của Steve Keen. Dấu chân đầu vào–đầu ra của Rogoff và Yang có thể dùng để ước tính tác động lên sản lượng.

## Mở rộng đại học năm 1999 và thất nghiệp thanh niên Trung Quốc

Các nghiên cứu thực nghiệm khác nhau về tác động việc làm. Danh mục chưa tìm thấy mô hình hình thức mở về thất nghiệp thanh niên. Hàng đợi cử nhân của Atlas là một ứng viên.

| Nghiên cứu | Kết quả | Ứng dụng |
| --- | --- | --- |
| [Knight, Deng và Li (2017)](https://econpapers.repec.org/RePEc:csa:wpaper:2016-04) | Tuyển sinh tăng gần sáu lần từ 1998 đến 2008. Lương tương đối giảm, thất nghiệp tăng, việc tốt giảm đối với nhóm mới. Người đang làm được bảo vệ | Kiểm tra khả năng tái tạo bảo vệ người trong hệ thống |
| [Ou và Zhao (2022)](https://econpapers.repec.org/RePEc:bla:chinae:v:30:y:2022:i:2:p:117-141) | Thất nghiệp nam và cử nhân giảm ngắn hạn. Tỷ lệ tham gia của nữ và thu nhập kỹ năng cao giảm | Kết quả đối chiếu, dùng khác biệt tỉnh và kiểm soát cầu Bartik |
| [Yu (2014)](https://dalspace.library.dal.ca/handle/10222/50406?show=full) | Thất nghiệp cử nhân trẻ tăng 8,7%, việc toàn thời gian giảm 21% | Kết quả đối chiếu từ CHNS |
| [Li, Whalley và Xing (2014)](https://econpapers.repec.org/RePEc:iza:izadps:dp4974) | Mở rộng làm tăng mạnh cơ hội vào đại học với mức tăng khác nhau giữa nhóm | Bổ sung phía tiếp cận đại học |

**Lưu ý dữ liệu**: tỷ lệ chính thức tuổi 16–24 chuyển sang loại người đang đi học từ 2023. Hai chuỗi không so trực tiếp. Đỉnh theo cách cũ là 21,3% tháng 6/2023. Theo cách mới, tháng 8/2026 là 18,9% ([bài báo](https://www.qatar-tribune.com/article/255654/business/chinas-youth-unemployment-hits-record-high-as-ai-deepens-job-crunch)).

**Mô hình chuẩn cần thêm**: “lake model” tìm việc và ghép việc của QuantEcon, chỉ có tỷ lệ tìm được việc và rời việc. Kiểm tra liệu các nhóm Tilly có giải thích thêm đỉnh tháng 7, chờ việc ngoài lực lượng lao động và bảo vệ người đang làm hay không.

## Học tập và bỏ học ở Philippines

Các mô hình đường học tập của Pritchett dùng dữ liệu nước thu nhập thấp và trung bình. Hoàn thành lớp 10 phổ cập làm tăng ít kết quả học, còn giảm tốc chương trình thêm tương đương 1,6 năm học. Điều này liên quan trực tiếp đến K–12, cải cách thêm hai năm học.

| Nghiên cứu | Cơ chế | Trạng thái |
| --- | --- | --- |
| [Beatty và Pritchett, tác hại của chương trình quá tham vọng (2012)](https://www.cesifo.org/DocDL/cesifo1_wp4040.pdf) | Trẻ học khi trình độ khớp với nội dung dạy. Chương trình quá nhanh làm phẳng đường học | Xây dựng từ phương trình bài báo |
| [Kaffenberger và Pritchett, mô hình động học tập (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7994294) | Hàm sư phạm tiềm năng hiệu chỉnh theo đường học quan sát | Xây dựng từ bài báo mở có tham số |
| [PIDS, trung học phổ thông và thị trường lao động](https://pidswebs.pids.gov.ph/CDN/INFOCUS/pidsupdates79.html) | Nam bỏ học hoặc trượt nhiều hơn nữ trong giáo dục cơ bản | Mục tiêu kiểm định |
| [Etulle và Carmelotes, mô phỏng bỏ học K–12 (2014)](https://rmrj.usjr.edu.ph/rmrj/index.php/RMRJ/article/view/99) | Dự báo 89% bỏ học trong K–12 | Dự báo thiếu khả tín, không dùng làm nền |

**Mô hình đề xuất**: kết hợp nhóm học sinh tái dựng của Atlas với hàm Pritchett để theo dõi ai tiếp tục học và học được bao nhiêu mỗi năm. Điều chỉnh tốc độ chương trình, phụ đạo và chuyển lớp 10 lên 11. Số liệu 2018 được trích dẫn cho thấy 18% học sinh trung học cơ sở không học tiếp lên trung học phổ thông ([nguồn](https://portal.amelica.org/ameli/journal/725/7253717004/html/)). Đầu ra là số năm học điều chỉnh theo kết quả và nghèo học tập, nối với LAYS.

**Câu hỏi mở**: chuỗi đánh giá nào ở Philippines phù hợp nhất để hiệu chỉnh theo lớp, kiểm tra quốc gia hay PISA 2018 và 2022?

## Các mô hình phát triển kinh điển cần xây dựng

Các mô hình giáo trình có phương trình sẵn, ước tính khoảng một ngày mỗi mô hình. Chúng làm chuẩn so sánh cho mô hình quốc gia.

| Mô hình | Cơ chế | Liên hệ |
| --- | --- | --- |
| Kinh tế hai khu vực Lewis | Lao động nông thôn dư chuyển sang khu vực hiện đại với lương cố định đến điểm ngoặt | Cung lao động Trung Quốc và Campuchia, lương nông thôn và Phnom Penh |
| Di cư Harris–Todaro | Di cư theo lương đô thị kỳ vọng, thất nghiệp có thể tăng khi thêm việc | Di cư Campuchia và hàng đợi cử nhân |
| [Doepke và Zilibotti, tiêu chuẩn lao động và lao động trẻ em](https://campuspress.yale.edu/zilibotti/published-research) | Kiểm tra tiêu chuẩn quốc tế có kéo dài lao động trẻ em không | Thực thi tuổi lao động tối thiểu ở Campuchia |
| Phân tách Schelling | Sở thích nhẹ về láng giềng gây phân tách mạnh | Chọn trường và phân tách |
| Bẫy nghèo | Hộ dưới ngưỡng vốn hoặc dinh dưỡng khó tự thoát bằng đầu tư | Lựa chọn hộ và giảm nợ ở Campuchia |
| Tín hiệu Spence và bệnh bằng cấp Dore | Bằng cấp sàng lọc lao động ngay cả khi không thêm kỹ năng, làm yêu cầu bằng cấp tăng | Ngưỡng bằng cấp và hàng đợi cử nhân |

**Câu hỏi mở**: mô hình nào nên dựa trên tác nhân, chẳng hạn Schelling hoặc Harris–Todaro với người di cư khác nhau, và mô hình nào nên dùng nghiệm đóng như Lewis hay Spence?

## Nguồn dữ liệu và thư viện hiện có

Atlas hướng tới so sánh các cơ chế phát triển và giáo dục trên cùng dữ liệu quốc gia ngay trong trình duyệt.

| Tài nguyên | Nội dung | Ứng dụng |
| --- | --- | --- |
| [Dữ liệu vốn con người Wittgenstein](https://iiasa.ac.at/models-tools-data/wcde) | Dân số theo tuổi, giới và học vấn cho 200 nước, bảy kịch bản đến 2100. Bản cũ tái dựng học vấn đến 1950 | Dữ liệu chung cho Trung Quốc, Philippines và Campuchia |
| [Thư viện mô hình CoMSES](https://comses.net/resources/standards) | Hơn 1.100 mô hình tác nhân có tài liệu ODD, chủ yếu NetLogo | Nguồn chuyển mã và chuẩn tài liệu ODD |
| [Cơ sở dữ liệu mô hình vĩ mô](https://www.macromodelbase.com/news-item/mmb-release-3-3) | Bản 3.3 có 161 mô hình cấu trúc vĩ mô trên một nền tảng | Mô hình Dynare nặng và tham khảo cách so sánh |
| ReplicationWiki | Tình trạng tái lập bài báo, gồm *Growing Like China* | Kiểm tra trước khi chuyển mã |
| Bài giảng QuantEcon | Mã Python và Julia mở về tăng trưởng, tìm việc và mô hình hồ | Chuẩn đối chiếu và giảng dạy |

**Giấy phép**: dẫn nguồn khi tự triển khai phương trình công bố. Kiểm tra giấy phép trước khi chuyển mã, hỏi tác giả nếu gói tái lập thiếu giấy phép.

## Danh sách xây dựng

Ưu tiên mô hình học tập Philippines vì phương trình đã công bố và nối được với hai mô hình hiện có.

| Hạng | Mô hình | Thời gian | Dữ liệu cần | Liên hệ | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| 1 | Đường học Pritchett và nhóm học sinh Philippines | 2–3 ngày | Đánh giá theo lớp và tỷ lệ chuyển cấp | Nhóm tái dựng, số năm học điều chỉnh | Chưa bắt đầu |
| 2 | Ba cơ chế tăng trưởng Trung Quốc rút gọn | 1–2 tuần | Chuỗi vĩ mô Chang và dữ liệu AER | Hàng đợi cử nhân Trung Quốc | Chưa bắt đầu |
| 3 | Tín dụng và bất động sản nhất quán tồn lượng–luồng | 1–2 tuần | Tổng tài trợ xã hội, thu từ đất và bảng đầu vào–đầu ra | Hấp thụ cử nhân và hàng đợi Trung Quốc | Chưa bắt đầu |
| 4 | Cú sốc nhóm Knight và mô hình hồ chuẩn | 2 ngày | Chuỗi thanh niên NBS có trong Atlas | Hàng đợi cử nhân Trung Quốc | Chưa bắt đầu |
| 5 | Dữ liệu Wittgenstein cho ba nước | 1 ngày | CSV WCDE | Campuchia, mô phỏng ngành và giáo viên | Chưa bắt đầu |
| 6 | Kiểm tra tiêu chuẩn lao động Doepke–Zilibotti | 2 ngày | Phương trình bài báo | Thực thi ở Campuchia | Chưa bắt đầu |
| 7 | Lewis, Harris–Todaro, Schelling, tín hiệu | Mỗi mô hình 1 ngày | Quy tắc giáo trình | Mô hình chuẩn thư viện | Chưa bắt đầu |

Ước tính gồm định nghĩa mô hình, bản dịch, rà soát điều khiển và kiểm tra theo quy trình Atlas.
