// SPDX-License-Identifier: GPL-2.0-only
/* Fixed Ace ramoops pmsg header observation; no writes to the pmsg header or payload. */
#include <linux/init.h>
#include <linux/module.h>
#include <linux/printk.h>
#include <linux/io.h>

#define ACE_PMSG_PA 0x48160000UL
#define ACE_HEADER_BYTES 12UL
#define ACE_PMSG_CAPACITY (0x10000UL - ACE_HEADER_BYTES)

static int __init ace_pmsg_header_init(void)
{
    void __iomem *mapping;
    u32 sig = 0, start = 0, size = 0;
    unsigned int attempt;
    bool stable = false;

    /* Same WC memory type as the observed ramoops mem_type=0 mapping.
     * Host preflight must establish the exact reserved resource first.
     * This neither requests ownership nor initializes/zaps the live ring. */
    mapping = ioremap_wc(ACE_PMSG_PA, ACE_HEADER_BYTES);
    if (!mapping) {
        pr_info("ACE_PMSG_HEADER: MAP_REFUSED\n");
        return -ENOMEM;
    }
    for (attempt = 0; attempt < 8; ++attempt) {
        sig = readl_relaxed(mapping);
        start = readl_relaxed(mapping + 4);
        size = readl_relaxed(mapping + 8);
        rmb();
        if (sig == readl_relaxed(mapping) &&
            start == readl_relaxed(mapping + 4) &&
            size == readl_relaxed(mapping + 8)) {
            stable = true;
            break;
        }
    }
    iounmap(mapping);
    /* Two matching observations are not a writer lock or atomic snapshot.
     * No payload bytes or virtual pointers are printed. */
    pr_info("ACE_PMSG_HEADER: sig=%08x start=%u size=%u capacity=%lu stable=%u valid=%u attempts=%u\n",
            sig, start, size, ACE_PMSG_CAPACITY, stable,
            stable && sig == 0x43474244U &&
            size <= ACE_PMSG_CAPACITY && start <= size,
            stable ? attempt + 1 : 8);
    return 0;
}
static void __exit ace_pmsg_header_exit(void) {}
module_init(ace_pmsg_header_init);
module_exit(ace_pmsg_header_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Read fixed Ace pmsg header; no pmsg or partition writes");
