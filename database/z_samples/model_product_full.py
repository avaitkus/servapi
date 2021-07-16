package quicktype

data class Welcome (
    id: Long,
    name: String,
    val slug: String,
    val permalink: String,
    val dateCreated: String,
    val dateCreatedGmt: String,
    val dateModified: String,
    val dateModifiedGmt: String,
    val type: String,
    val status: String,
    val featured: Boolean,
    val catalogVisibility: String,
    description: String,
    val shortDescription: String,
    sku: String,
    val price: String,
    val regularPrice: String,
    val salePrice: String,
    val dateOnSaleFrom: Any? = null,
    val dateOnSaleFromGmt: Any? = null,
    val dateOnSaleTo: Any? = null,
    val dateOnSaleToGmt: Any? = null,
    val onSale: Boolean,
    val purchasable: Boolean,
    val totalSales: Long,
    val virtual: Boolean,
    val downloadable: Boolean,
    val downloads: List<Any?>,
    val downloadLimit: Long,
    val downloadExpiry: Long,
    val externalURL: String,
    val buttonText: String,
    val taxStatus: String,
    val taxClass: String,
    val manageStock: Boolean,
    val stockQuantity: Long,
    val backorders: String,
    val backordersAllowed: Boolean,
    val backordered: Boolean,
    val soldIndividually: Boolean,
    weight: String,
    dimensions: Dimensions,
    val shippingRequired: Boolean,
    val shippingTaxable: Boolean,
    val shippingClass: String,
    val shippingClassID: Long,
    val reviewsAllowed: Boolean,
    val averageRating: String,
    val ratingCount: Long,
    val upsellIDS: List<Long>,
    val crossSellIDS: List<Long>,
    val parentID: Long,
    val purchaseNote: String,
    categories: List<Category>,
    val tags: List<Category>,
    images: List<Image>,
    attributes: List<Attribute>,
    val defaultAttributes: List<Any?>,
    val variations: List<Any?>,
    val groupedProducts: List<Any?>,
    val menuOrder: Long,
    val priceHTML: String,
    val relatedIDS: List<Long>,
    metaData: List<MetaDatum>,
    val stockStatus: String,
    val yoastHead: String,
    translations: Translations,
    lang: String,
    val links: Links
)

data class Attribute (
    val id: Long,
    val name: String,
    val position: Long,
    val visible: Boolean,
    val variation: Boolean,
    val options: List<String>
)

data class Category (
    val id: Long,
    val name: String,
    val slug: String
)

data class Dimensions (
    val length: String,
    val width: String,
    val height: String
)

data class Image (
    val id: Long,
    val dateCreated: String,
    val dateCreatedGmt: String,
    val dateModified: String,
    val dateModifiedGmt: String,
    val src: String,
    val name: String,
    val alt: String
)

data class Links (
    val self: List<Collection>,
    val collection: List<Collection>
)

data class Collection (
    val href: String
)

data class MetaDatum (
    val id: Long,
    val key: String,
    val value: String
)

data class Translations (
    val en: String,
    val et: String,
    val lt: String,
    val lv: String,
    val ru: String
)
